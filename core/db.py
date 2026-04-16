import os
import psycopg2
from urllib.parse import urlparse


def get_db_conn():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    host = urlparse(database_url).hostname

    print("Now App connected to:", host)

    return psycopg2.connect(database_url)
