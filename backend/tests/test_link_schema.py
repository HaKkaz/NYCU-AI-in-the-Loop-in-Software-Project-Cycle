import sqlite3
import unittest
from datetime import datetime, timedelta
from pathlib import Path


V1 = Path(__file__).resolve().parents[1] / "migrations" / "0001_create_link_tables.sql"


class LinkSchemaTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(V1.read_text(encoding="utf-8"))

    def link(self, decision="2026-09-21-example", pr=3):
        return self.db.execute(
            "INSERT INTO link (decision_id, pr_number, created_by) VALUES (?, ?, 'Alex')",
            (decision, pr),
        ).lastrowid

    def event(self, link_id, actor, action, comment=None):
        self.db.execute(
            "INSERT INTO link_event (link_id, actor, action, comment) VALUES (?, ?, ?, ?)",
            (link_id, actor, action, comment),
        )

    def test_f4_link_starts_pending_with_utc_timestamps(self):
        link_id = self.link()
        status, creator, created, updated = self.db.execute(
            "SELECT status, created_by, created_at, updated_at FROM link WHERE id = ?",
            (link_id,),
        ).fetchone()
        self.assertEqual((status, creator, created), ("pending", "Alex", updated))
        self.assertEqual(datetime.fromisoformat(created.replace("Z", "+00:00")).utcoffset(), timedelta(0))

    def test_f4_f8_unique_active_pair_released_by_withdrawal(self):
        link_id = self.link()
        self.link(pr=4)
        self.link(decision="2026-09-30-other-decision")
        for status in ("pending", "confirmed", "disputed"):
            with self.subTest(status=status):
                self.db.execute("UPDATE link SET status = ? WHERE id = ?", (status, link_id))
                with self.assertRaises(sqlite3.IntegrityError):
                    self.link()
        for _ in range(2):
            self.db.execute("UPDATE link SET status = 'withdrawn' WHERE id = ?", (link_id,))
            link_id = self.link()
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM link").fetchone(), (5,))

    def test_f6_f7_only_dispute_and_respond_require_nonblank_comments(self):
        link_id = self.link()
        self.event(link_id, "Alex", "create")
        self.event(link_id, "Sam", "confirm")
        for actor, action in (("Sam", "dispute"), ("Alex", "respond")):
            for comment in (None, "", " ", "\t\r\n", "\u00a0\u3000"):
                with self.subTest(action=action, comment=comment):
                    with self.assertRaises(sqlite3.IntegrityError):
                        self.event(link_id, actor, action, comment)
            self.event(link_id, actor, action, "  請看 PR #5。  ")
        self.event(link_id, "Alex", "withdraw")
        comments = self.db.execute(
            "SELECT comment FROM link_event WHERE link_id = ? ORDER BY id", (link_id,)
        ).fetchall()
        self.assertEqual(comments, [(None,), (None,), ("  請看 PR #5。  ",), ("  請看 PR #5。  ",), (None,)])

    def test_section_8_rejects_invalid_status_and_action(self):
        link_id = self.link()
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("UPDATE link SET status = 'accepted' WHERE id = ?", (link_id,))
        with self.assertRaises(sqlite3.IntegrityError):
            self.event(link_id, "Sam", "edit")

    def test_f9_requires_link_and_protects_referenced_parent(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.event(999, "Alex", "create")
        link_id = self.link()
        self.event(link_id, "Alex", "create")
        at = self.db.execute("SELECT at FROM link_event").fetchone()[0]
        self.assertEqual(datetime.fromisoformat(at.replace("Z", "+00:00")).utcoffset(), timedelta(0))
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("DELETE FROM link WHERE id = ?", (link_id,))
