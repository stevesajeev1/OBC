import psycopg
from ..util.db import get_db_connection
from ..models.profile import ProfilePublic, ProfileUpdate, Internship


# profile READ functions

def get_raw_profile_data(username: str):
    """gets the raw profile data as a dict."""

    conn = get_db_connection();
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT username, full_name, major, grad_year, 
                    linkedin_link, bio, prev_internships
                FROM users 
                WHERE username = %s
                """,
                (username,),
            )
            record = cur.fetchone()
            if record:
                return {
                    "username": record[0], 
                    "full_name": record[1], 
                    "major": record[2],
                    "grad_year": record[3], 
                    "linkedin_link": record[4], 
                    "bio": record[5],
                    "prev_internships": record[6],
                }
    except psycopg.Error as e:
        print(f"Database error in get_raw_profile_data: {e}")
    finally:
        if conn:
            conn.close()
    return None


def get_public_profile(username:str):
    """gets a users profile and check if complete"""
    profile_data = get_raw_profile_data(username)

    if not profile_data:
        return None
    
    try:
        public_profile = ProfilePublic(**profile_data)
        return public_profile
    except Exception:
        # means profile is not complete
        return None
    


# profile WRITE functions
def update_profile(username:str, profile_update:ProfileUpdate):
    """updates a user profile in the db"""

    # get current data
    current_data = get_raw_profile_data(username)
    if not current_data:
        return None
    
    # make update model from current data
    current_profile = ProfileUpdate(**current_data)

    # apply new data
    update_data = profile_update.model_dump(exclude_unset=True)

    # merge new data and current data
    updated_profile = current_profile.model_copy(update=update_data)

    # convert internship list to dict
    internships_list = None
    if updated_profile.prev_internships is not None:
        internships_list = [i.model_dump() for i in updated_profile.prev_internships]

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET full_name = %s, major = %s, grad_year = %s, 
                    linkedin_link = %s, bio = %s, prev_internships = %s
                WHERE username = %s
                """,
                (
                    updated_profile.full_name,
                    updated_profile.major,
                    updated_profile.grad_year,
                    str(updated_profile.linkedin_link) if updated_profile.linkedin_link else None,
                    updated_profile.bio,
                    internships_list, 
                    username,
                ),
            )
            conn.commit()
            
            # After updating, fetch the new profile data to return it
            return get_raw_profile_data(username)
    except psycopg.Error as e:
        conn.rollback()
        print(f"Database error in update_profile_in_db: {e}")
        return None
    finally:
        if conn:
            conn.close()
