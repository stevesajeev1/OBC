from uuid import UUID

from ..models.cron import Listing
from ..util.db import get_db_connection


def get_listings_from_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id, source, company_name, title, active,
                    date_updated, is_visible, date_posted, url,
                    locations, company_url, terms, sponsorship,
                    category, faang_plus, company_logo
                FROM listings;
            """
            )

            rows = cur.fetchall()

            listings = [Listing.from_tuple(row) for row in rows]
            return listings


def delete_listing_in_db(listing_id: UUID):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM listings
                WHERE id = %s
                RETURNING id;
                """,
                (listing_id,),
            )
            deleted = cur.fetchone()

    return deleted is not None
