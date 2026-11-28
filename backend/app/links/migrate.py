"""Apply numbered SQL migrations, or check the version without changing the database."""

import argparse
from pathlib import Path
import sqlite3
import sys

from .db import connect

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"


def apply_sql(db: sqlite3.Connection, script: Path) -> None:
    # executescript() implicitly commits pending transactions on older Python versions.
    # Let SQLite identify statement boundaries, including semicolons inside triggers.
    sql = script.read_text(encoding="utf-8")
    start = 0
    for end, char in enumerate(sql, 1):
        if char == ";" and sqlite3.complete_statement(sql[start:end]):
            db.execute(sql[start:end])
            start = end
    if sql[start:].strip():
        db.execute(sql[start:])


def schema_version(db: sqlite3.Connection, latest: int) -> int:
    version = db.execute("PRAGMA user_version").fetchone()[0]
    if not 0 <= version <= latest:
        raise ValueError(f"Unsupported database version {version}. This build supports 0 through {latest}.")
    return version


def migrate(
    database_url: str | None = None,
    migrations_dir: Path = MIGRATIONS_DIR,
    *,
    check_only: bool = False,
) -> int:
    scripts = sorted(migrations_dir.glob("*.sql"))
    if not scripts:
        raise ValueError(f"No SQL migrations found in {migrations_dir}.")
    for version, script in enumerate(scripts, 1):
        if not script.name.startswith(f"{version:04d}_"):
            raise ValueError(f"Expected migration {version:04d}, found {script.name}.")

    latest = len(scripts)
    with connect(database_url, read_only=check_only) as db:
        current = schema_version(db, latest)
        if current == latest:
            return current
        if check_only:
            raise ValueError(f"Database version is {current}, expected {latest}. Run migrations first.")

        # Another process may complete the upgrade while we wait for the writer lock.
        db.execute("BEGIN IMMEDIATE")
        current = schema_version(db, latest)
        for version, script in enumerate(scripts[current:], current + 1):
            try:
                apply_sql(db, script)
            except sqlite3.Error as exc:
                raise ValueError(f"Migration {script.name} failed: {exc}") from exc
            db.execute(f"PRAGMA user_version = {version}")
        # connect() commits the schema and version together, or rolls both back.
    return latest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="require the latest schema without applying migrations")
    args = parser.parse_args()
    try:
        version = migrate(check_only=args.check)
    except (OSError, ValueError, sqlite3.Error) as exc:
        print(f"Database migration: {exc}", file=sys.stderr)
        return 1
    print(f"Database schema is at version {version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
