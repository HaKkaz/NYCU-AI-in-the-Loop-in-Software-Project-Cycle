from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
import os
import sqlite3
from tempfile import TemporaryDirectory
from threading import Barrier
import unittest

from unittest.mock import patch

from app.links.db import connect, database_path
from app.links.migrate import migrate


class MigrationTests(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.scripts = root / "migrations"
        self.scripts.mkdir()
        self.db = root / "data" / "app.db"
        self.url = f"sqlite:///{self.db}"
        (self.scripts / "0001_sample.sql").write_text("CREATE TABLE sample (value TEXT);")

    def migrate(self, *, check_only=False):
        return migrate(self.url, self.scripts, check_only=check_only)

    def query(self, sql):
        with closing(sqlite3.connect(self.db)) as db, db:
            return db.execute(sql).fetchall()

    def test_relative_and_absolute_file_urls(self):
        self.assertEqual(database_path("sqlite:///./data/app.db"), Path("data/app.db"))
        self.assertEqual(database_path(self.url), self.db)
        for url in ("sqlite:///:memory:", "sqlite:///", "postgresql://localhost/db"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                database_path(url)

    def test_check_is_read_only_and_upgrading_preserves_data(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.migrate(check_only=True)
        self.assertFalse(self.db.parent.exists())
        self.assertEqual(self.migrate(), 1)
        self.query("INSERT INTO sample VALUES ('first')")
        before = self.db.read_bytes()
        (self.scripts / "0002_sample.sql").write_text("INSERT INTO sample VALUES ('semi;colon');")
        with self.assertRaisesRegex(ValueError, "expected 2"):
            self.migrate(check_only=True)
        self.assertEqual(self.db.read_bytes(), before)
        self.assertEqual(self.migrate(), 2)
        self.assertEqual(self.migrate(), 2)
        self.assertEqual(self.migrate(check_only=True), 2)
        self.assertEqual(self.query("SELECT value FROM sample ORDER BY rowid"), [("first",), ("semi;colon",)])

    def test_failed_migration_rolls_back_ddl_data_and_version_then_retries(self):
        self.migrate()
        script = self.scripts / "0002_more.sql"
        script.write_text(
            "CREATE TABLE more (id INTEGER); INSERT INTO sample VALUES ('partial');"
            "INSERT INTO nonexistent VALUES (42);"
        )
        with self.assertRaisesRegex(ValueError, "0002_more.sql"):
            self.migrate()
        self.assertEqual(self.query("SELECT name FROM sqlite_master WHERE type = 'table'"), [("sample",)])
        self.assertEqual(self.query("SELECT * FROM sample"), [])
        self.assertEqual(self.query("PRAGMA user_version"), [(1,)])
        script.write_text("CREATE TABLE more (id INTEGER);")
        self.assertEqual(self.migrate(), 2)

    def test_unversioned_table_collision_preserves_existing_data(self):
        self.db.parent.mkdir()
        self.query("CREATE TABLE sample (old_value INTEGER)")
        self.query("INSERT INTO sample VALUES (7)")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.migrate()
        self.assertEqual(self.query("SELECT old_value FROM sample"), [(7,)])
        self.assertEqual(self.query("PRAGMA user_version"), [(0,)])

    def test_rejects_newer_database_and_gaps_in_migrations(self):
        self.migrate()
        self.query("PRAGMA user_version = 42")
        for check_only in (False, True):
            with self.subTest(check_only=check_only), self.assertRaisesRegex(ValueError, "version 42"):
                self.migrate(check_only=check_only)
        self.assertEqual(self.query("PRAGMA user_version"), [(42,)])
        (self.scripts / "0003_skip.sql").write_text("SELECT 1;")
        with self.assertRaisesRegex(ValueError, "Expected migration 0002"):
            self.migrate()

    def test_concurrent_runners_apply_each_migration_once(self):
        (self.scripts / "0002_init.sql").write_text("INSERT INTO sample VALUES ('once');")
        ready = Barrier(3)

        def start(_):
            ready.wait(timeout=10)
            return self.migrate()

        with ThreadPoolExecutor(max_workers=3) as pool:
            self.assertEqual(list(pool.map(start, range(3))), [2, 2, 2])
        self.assertEqual(self.query("SELECT * FROM sample"), [("once",)])

    def test_store_and_migrator_share_environment_and_transaction_semantics(self):
        with patch.dict(os.environ, {"DATABASE_URL": self.url}):
            self.assertEqual(migrate(migrations_dir=self.scripts), 1)
            with connect() as db:
                self.assertEqual(db.execute("PRAGMA foreign_keys").fetchone()[0], 1)
                db.execute("CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES child(id))")
            with self.assertRaises(sqlite3.IntegrityError), connect() as db:
                db.execute("INSERT INTO child (id) VALUES (1)")
                db.execute("INSERT INTO child VALUES (2, 100)")
            with connect(read_only=True) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) AS n FROM child").fetchone()["n"], 0)
                with self.assertRaises(sqlite3.OperationalError):
                    db.execute("INSERT INTO child (id) VALUES (3)")

    def test_current_schema_needs_no_write_lock_at_startup(self):
        self.migrate()
        with connect(self.url) as writer:
            writer.execute("BEGIN IMMEDIATE")
            self.assertEqual(self.migrate(), 1)


class ShippedMigrationsTests(unittest.TestCase):
    def test_empty_database_and_repeat(self):
        with TemporaryDirectory() as directory:
            url = f"sqlite:///{Path(directory) / 'timeline.db'}"
            self.assertEqual(migrate(url), 2)
            with connect(url) as db:
                tables = {row[0] for row in db.execute("SELECT name FROM sqlite_schema WHERE type = 'table'")}
                self.assertEqual(tables, {"link", "link_event"})
                db.execute("INSERT INTO link (decision_id, pr_number, created_by) VALUES (?, ?, ?)", ("sample", 1, "A"))
            self.assertEqual(migrate(url), 2)
            with connect(url, read_only=True) as db:
                self.assertEqual(db.execute("PRAGMA user_version").fetchone()[0], 2)
                self.assertEqual(db.execute("SELECT count(*) FROM link").fetchone()[0], 1)
