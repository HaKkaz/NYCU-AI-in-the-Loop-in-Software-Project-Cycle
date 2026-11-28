import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.links.db import connect
from app.links.migrate import MIGRATIONS_DIR, migrate
from app.main import app


class SchemaStartupTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.url = f"sqlite:///{self.root / 'data' / 'app.db'}"
        self.enterContext(patch.dict(os.environ, DATABASE_URL=self.url))

    def test_startup_and_restart_on_empty_database(self):
        for _ in range(2):
            with TestClient(app) as client:
                self.assertEqual(client.get("/openapi.json").status_code, 200)
                self.assertEqual(migrate(check_only=True), 2)

    def test_startup_upgrades_v1_and_preserves_link_history_on_restart(self):
        v1 = self.root / "v1"
        v1.mkdir()
        first = MIGRATIONS_DIR / "0001_create_link_tables.sql"
        (v1 / first.name).write_bytes(first.read_bytes())
        self.assertEqual(migrate(migrations_dir=v1), 1)
        with connect() as db:
            db.execute("INSERT INTO link (decision_id, pr_number, created_by) VALUES (?, ?, ?)", ("d", 1, "A"))
        for _ in range(2):
            with TestClient(app), connect(read_only=True) as db:
                self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 2)
                events = db.execute("SELECT actor, action FROM link_event ORDER BY id").fetchall()
                self.assertEqual([tuple(row) for row in events], [("A", "create")])

    def test_future_version_and_failed_migration_block_fastapi(self):
        with connect() as db:
            db.execute("CREATE TABLE link (legacy_value TEXT)")
            db.execute("INSERT INTO link VALUES (?)", ("keep",))
        for version, error in ((0, "already exists"), (99, "Unsupported database version")):
            with self.subTest(version=version):
                with connect() as db:
                    db.execute(f"PRAGMA user_version = {version}")
                with self.assertRaisesRegex(ValueError, error), TestClient(app):
                    pass
                with connect(read_only=True) as db:
                    self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], version)
                    self.assertEqual(db.execute("SELECT legacy_value FROM link").fetchone()[0], "keep")
