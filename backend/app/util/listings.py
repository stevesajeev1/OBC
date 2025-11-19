from uuid import UUID

from ..models.listings import Listing
from ..util.db import get_db_connection


def get_listings_from_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    l.id, l.source, l.title, l.active,
                    l.date_updated, l.is_visible, l.date_posted, l.url,
                    l.locations, l.terms, l.sponsorship,
                    l.category, l.faang_plus,
                    c.id AS company_id, c.name, c.url, c.logo_url
                FROM listings l
                LEFT JOIN companies c ON l.company_id = c.id;
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

            

