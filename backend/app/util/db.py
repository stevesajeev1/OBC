import os

import psycopg
from dotenv import load_dotenv
from fastapi import HTTPException, status
from psycopg_pool import ConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

pool = ConnectionPool(
    conninfo=DATABASE_URL, min_size=1, max_size=10, connection_class=psycopg.Connection
)


def get_db_connection():
    try:
        return pool.connection()
    except psycopg.OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to the database: {e}",
        )
