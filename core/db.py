import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_conn():
    """Get PostgreSQL database connection."""

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")

    if not all([dbname, user, password, host, port]):
        raise ValueError("Missing one or more database environment variables.")

    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=int(port),
    )
