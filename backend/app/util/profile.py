import psycopg
from psycopg.rows import dict_row

from ..models.profile import Internship, Profile, ProfileUpdate
from ..util.db import get_db_connection

# profile READ functions


def get_profile_id(username: str):
    """gets the foreign key (profile_id) from users table"""

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT profile_id FROM users WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return row[0]  # returns the profile_id
    return None


def get_valid_profile(username: str):
    """gets a users profile and check if complete"""

    profile_id = get_profile_id(username)

    if not profile_id:
        return None

    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # get profile data
                cur.execute(
                    """
                    SELECT id, full_name, major, grad_year, linkedin_url, bio, image_url
                    FROM profiles WHERE id = %s
                    """,
                    (profile_id,),
                )
                profile_row = cur.fetchone()

                if not profile_row:
                    return None

                # get internship data
                cur.execute(
                    """
                    SELECT company, role, time_period 
                    FROM internships WHERE profile_id = %s
                    """,
                    (profile_id,),
                )
                internship_rows = cur.fetchall()

                return Profile.from_db(profile_row, internship_rows)

    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None


# helper for getting all profiles
def get_all_profiles(page: int, limit: int):
    """gets a paginated list of profiles"""

    offset = (page - 1) * limit

    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # get main profile rows
                cur.execute(
                    """
                    SELECT id, full_name, major, grad_year, linkedin_url, bio, image_url
                    FROM profiles
                    ORDER BY id DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset),
                )
                profile_rows = cur.fetchall()

                results = []
                for row in profile_rows:
                    # for each profile, get internships
                    cur.execute(
                        """
                        SELECT company, role, time_period 
                        FROM internships WHERE profile_id = %s
                        """,
                        (row["id"],),
                    )
                    internship_rows = cur.fetchall()

                    results.append(Profile.from_db(row, internship_rows))

                return results

    except Exception as e:
        print(f"Error getting all profiles: {e}")
        return []


# profile WRITE functions


def update_profile(username: str, profile_update: ProfileUpdate):
    """updates a user profile in the db (including profile and internship)"""

    try:

        profile_id = get_profile_id(username)

        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                # create profile if doesnt exist
                if not profile_id:
                    cur.execute(
                        "INSERT INTO profiles (full_name) VALUES (NULL) RETURNING id"
                    )
                    new_row = cur.fetchone()
                    profile_id = new_row["id"]

                    cur.execute(
                        "UPDATE users SET profile_id = %s WHERE username = %s",
                        (profile_id, username),
                    )

                update_data = profile_update.model_dump(exclude_unset=True)

                fields_map = {
                    "full_name": "full_name",
                    "major": "major",
                    "grad_year": "grad_year",
                    "linkedin_link": "linkedin_url",
                    "bio": "bio",
                    "image_url": "image_url",
                }

                set_clauses = []
                values = []

                for model_field, db_col in fields_map.items():
                    if model_field in update_data:
                        set_clauses.append(f"{db_col} = %s")
                        values.append(update_data[model_field])

                if set_clauses:
                    values.append(profile_id)
                    sql = f"UPDATE profiles SET {', '.join(set_clauses)} WHERE id = %s"
                    cur.execute(sql, values)

                # changing internships
                if (
                    "prev_internships" in update_data
                    and update_data["prev_internships"] is not None
                ):
                    # delete existing internships for this profile
                    cur.execute(
                        "DELETE FROM internships WHERE profile_id = %s", (profile_id,)
                    )

                    # innsert new ones one by one
                    for internship in update_data["prev_internships"]:
                        cur.execute(
                            """
                            INSERT INTO internships (profile_id, company, role, time_period)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                profile_id,
                                internship["company"],
                                internship["role"],
                                internship["time_period"],
                            ),
                        )

                conn.commit()

            return get_valid_profile(username)

    except Exception as e:
        print(f"Database error in update_profile: {e}")
        return None
