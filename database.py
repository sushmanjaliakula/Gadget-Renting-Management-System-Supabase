
import psycopg
from psycopg.rows import dict_row
from config import Config


def get_db_connection():
    """Connect to the Supabase PostgreSQL database."""

    if not Config.DATABASE_URL:
        raise psycopg.OperationalError(
            "DATABASE_URL is missing. Check your environment configuration."
        )

    return psycopg.connect(
        Config.DATABASE_URL,
        connect_timeout=15,
        sslmode="require",
        row_factory=dict_row
    )


def fetch_all(query, params=None):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    finally:
        connection.close()


def fetch_one(query, params=None):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()
    finally:
        connection.close()
