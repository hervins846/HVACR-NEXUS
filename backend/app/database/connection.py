from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3
from typing import Iterator


DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "hvacr_nexus.db"


def get_database_url() -> str:
    return os.getenv("HVACR_DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")


def get_sqlite_path() -> str:
    url = get_database_url()
    if url.startswith("sqlite:///"):
        db_file = Path(url.replace("sqlite:///", "", 1))
        db_file.parent.mkdir(parents=True, exist_ok=True)
        return str(db_file)
    DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return str(DEFAULT_DB_PATH)


def create_sqlite_connection(timeout: float = 10.0) -> sqlite3.Connection:
    conn = sqlite3.connect(get_sqlite_path(), timeout=timeout, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_db_connection() -> Iterator[sqlite3.Connection]:
    conn = create_sqlite_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()