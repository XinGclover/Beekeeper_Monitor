from collections.abc import Generator

from core.db import get_db_conn


def get_db_connection() -> Generator:
    conn = get_db_conn()
    try:
        yield conn
    finally:
        conn.close()