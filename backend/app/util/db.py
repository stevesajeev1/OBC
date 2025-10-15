import os

import psycopg2
from dotenv import load_dotenv
from fastapi import HTTPException, status

# --- load env file ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# --- db functions ---
def get_db_connection():
    """establish connection with the NeonDB Postgres DB."""
    if not DATABASE_URL:
        # needs database connection string.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="DATABASE_URL environment variable is not set. Please check your server configuration.",
        )
    try:
        # psycopg2 can connect directly using the connection URI provided by Neon.
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to the database: {e}",
        )
