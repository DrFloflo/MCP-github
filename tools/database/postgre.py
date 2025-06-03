from psycopg import connect as pg_connect
from psycopg.sql import SQL

from core.config import settings
from core.logger import logger

def connect():
    """Create a connection to the PostgreSQL database."""
    try:
        conn = pg_connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            autocommit=True  # Equivalent to ISOLATION_LEVEL_AUTOCOMMIT
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None

def read_db(query):
    """
    Read a database from a PostgreSQL server.

    Args:
        query (str): The query to execute.

    Returns:
        list: A list of rows from the database.
    """
    conn = connect()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(SQL(query))
            return cur.fetchall()
    except Exception as e:
        logger.error(f"Failed to execute query: {e}")
        return None