from .db import get_db_connection
from ..models.favorites import Favorite
from ..models.listings import Listing

from uuid import UUID

def save_favorite_to_db(user_id : int, listing_id: UUID) -> bool:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO favorites (user_id, listing_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, listing_id) DO NOTHING
                RETURNING user_id;
                """,
                (user_id, listing_id)
            )
            inserted = cur.fetchone()
            conn.commit()

    return inserted is not None
    

def get_favorites_from_db(user_id: int) ->list[Listing]:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    l.id, l.source, l.title, l.active, l.date_updated, l.is_visible, l.date_posted, l.url, l.locations, l.terms, l.sponsorship, l.category, l.faang_plus,
                    c.id AS company_id, c.name, c.url, c.logo_url
                FROM listings l
                JOIN favorites f ON l.id = f.listing_id
                LEFT JOIN companies c ON l.company_id = c.id
                WHERE f.user_id = %s;
                """,
                (user_id,),
            )

            rows = cur.fetchall()

            favorites = [Listing.from_tuple(row) for row in rows]
            return favorites
        
def delete_favorite_from_db(user_id : int, listing_id : UUID) -> bool:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM favorites
                WHERE user_id = %s AND listing_id = %s
                RETURNING user_id;
                """,
                (user_id, listing_id),
            )
            deleted = cur.fetchone()
            conn.commit()
    return deleted is not None

