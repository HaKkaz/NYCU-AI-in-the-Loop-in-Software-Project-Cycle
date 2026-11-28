import os
import sqlite3
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
        self.db_path = self.root / "data" / "app.db"
        self.enterContext(patch.dict(os.environ, DATABASE_URL=f"sqlite:///{self.db_path}"))

    def test_missing_database_blocks_startup_without_creating_files(self):
        with self.assertRaises(sqlite3.OperationalError), TestClient(app):
            pass
        self.assertFalse(self.db_path.parent.exists())

    def test_v1_blocks_startup_until_migration_service_upgrades_it(self):
        v1 = self.root / "v1"
        v1.mkdir()
        first = MIGRATIONS_DIR / "0001_create_link_tables.sql"
        (v1 / first.name).write_bytes(first.read_bytes())
        self.assertEqual(migrate(migrations_dir=v1), 1)
        with connect() as db:
            db.execute("INSERT INTO link (decision_id, pr_number, created_by) VALUES (?, ?, ?)", ("d", 1, "A"))

        before = self.db_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "expected 2"), TestClient(app):
            pass
        self.assertEqual(self.db_path.read_bytes(), before)

        self.assertEqual(migrate(), 2)
        after = self.db_path.read_bytes()
        for _ in range(2):
            with TestClient(app) as client:
                self.assertEqual(client.get("/openapi.json").status_code, 200)
            self.assertEqual(self.db_path.read_bytes(), after)
        with connect(read_only=True) as db:
            events = db.execute("SELECT actor, action FROM link_event ORDER BY id").fetchall()
            self.assertEqual([tuple(row) for row in events], [("A", "create")])

    def test_future_version_blocks_startup_and_is_preserved(self):
        with connect() as db:
            db.execute("PRAGMA user_version = 99")
        before = self.db_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "Unsupported database version 99"), TestClient(app):
            pass
        self.assertEqual(self.db_path.read_bytes(), before)
