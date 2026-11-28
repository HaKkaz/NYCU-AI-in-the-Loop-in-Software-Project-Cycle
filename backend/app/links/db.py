"""Shared SQLite connections for migrations and the Link store."""

from collections.abc import Iterator
from contextlib import closing, contextmanager
import os
from pathlib import Path
import sqlite3

DEFAULT_DATABASE_URL = "sqlite:///./data/app.db"


def database_path(url: str) -> Path:
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        raise ValueError("DATABASE_URL must be a sqlite:/// file URL.")
    path = url[len(prefix):]
    if not path or path == ":memory:" or "?" in path or path.startswith("file:"):
        raise ValueError("DATABASE_URL must point to a persistent SQLite file without URI options.")
    return Path(path)


@contextmanager
def connect(database_url: str | None = None, *, read_only: bool = False) -> Iterator[sqlite3.Connection]:
    """Yield named rows and commit writes on success, rolling them back on errors.

    For a Link transition, BEGIN IMMEDIATE before reading its state, then update
    the Link and insert the LinkEvent on this same connection.
    """
    url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL) if database_url is None else database_url
    path = database_path(url)
    if not read_only:
        path.parent.mkdir(parents=True, exist_ok=True)
    mode = "ro" if read_only else "rwc"
    uri = f"{path.resolve().as_uri()}?mode={mode}"
    with closing(sqlite3.connect(uri, uri=True, timeout=30)) as db:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        with db:
            yield db
