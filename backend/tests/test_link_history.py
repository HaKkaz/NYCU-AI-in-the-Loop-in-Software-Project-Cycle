import sqlite3
import unittest
from datetime import datetime, timedelta
from pathlib import Path


MIGRATIONS = Path(__file__).resolve().parents[1] / "migrations"
CREATED_AT = "2026-09-21T11:30:00Z"


class LinkHistoryTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.execute("PRAGMA foreign_keys = ON")
        v1 = MIGRATIONS / "0001_create_link_tables.sql"
        self.db.executescript(v1.read_text(encoding="utf-8"))
        self.db.execute(
            "INSERT INTO link (decision_id, pr_number, created_by, created_at, updated_at) "
            "VALUES ('decision', 3, 'Alex', ?, ?)", (CREATED_AT, CREATED_AT)
        )

    def upgrade(self):
        self.db.executescript((MIGRATIONS / "0002_link_history.sql").read_text(encoding="utf-8"))

    def test_f9_backfills_missing_create_and_preserves_existing_events(self):
        self.db.execute(
            "INSERT INTO link (decision_id, pr_number, created_by, status) "
            "VALUES ('decision', 4, 'Sam', 'confirmed')"
        )
        self.db.executemany(
            "INSERT INTO link_event (link_id, actor, action, comment, at) VALUES (?, ?, ?, ?, ?)",
            [
                (2, "Sam", "create", "Relevant PR", "2026-09-21T09:00:00Z"),
                (2, "Alex", "confirm", None, "2026-09-21T09:10:00Z"),
            ],
        )
        existing = self.db.execute("SELECT * FROM link_event ORDER BY id").fetchall()
        self.upgrade()
        preserved = self.db.execute("SELECT * FROM link_event WHERE link_id = 2 ORDER BY id")
        self.assertEqual(preserved.fetchall(), existing)
        recovered = self.db.execute(
            "SELECT actor, action, comment, at FROM link_event WHERE link_id = 1"
        ).fetchall()
        self.assertEqual(recovered, [("Alex", "create", None, CREATED_AT)])
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO link_event (link_id, actor, action) VALUES (1, 'Alex', 'create')"
            )

    def test_f9_legacy_duplicate_create_fails_without_losing_events(self):
        self.db.executemany(
            "INSERT INTO link_event (link_id, actor, action, comment) VALUES (1, 'Alex', 'create', ?)",
            [("first",), ("second",)],
        )
        with self.assertRaises(sqlite3.IntegrityError):
            self.upgrade()
        self.assertEqual(
            self.db.execute("SELECT comment FROM link_event ORDER BY id").fetchall(),
            [("first",), ("second",)],
        )

    def test_section_8_timestamp_updates_only_on_status_change(self):
        self.upgrade()
        self.db.execute("UPDATE link SET status = 'pending' WHERE id = 1")
        self.assertEqual(self.db.execute("SELECT updated_at FROM link").fetchone(), (CREATED_AT,))
        self.db.execute("UPDATE link SET status = 'confirmed' WHERE id = 1")
        updated_at = self.db.execute("SELECT updated_at FROM link").fetchone()[0]
        self.assertNotEqual(updated_at, CREATED_AT)
        updated_utc = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        self.assertEqual(updated_utc.utcoffset(), timedelta(0))

        explicit_time = "2026-11-28T10:17:00.421Z"
        self.db.execute(
            "UPDATE link SET status = 'disputed', updated_at = ? WHERE id = 1", (explicit_time,)
        )
        self.assertEqual(self.db.execute("SELECT updated_at FROM link").fetchone(), (explicit_time,))
