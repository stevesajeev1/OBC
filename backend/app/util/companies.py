from ..models.companies import Company
from .db import get_db_connection


def get_companies_from_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, url, logo_url FROM companies;
                """
            )

            rows = cur.fetchall()

            companies = [Company.from_tuple(row) for row in rows]
            return companies

