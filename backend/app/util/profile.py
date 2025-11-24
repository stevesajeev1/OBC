import psycopg
from psycopg.rows import dict_row

from ..models.auth import User
from ..models.profile import Internship, Profile, ProfileUpdate
from ..util.db import get_db_connection

# profile READ functions


def get_profile_id(username: str):
    """gets the foreign key (profile_id) from users table"""

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.id
                FROM profiles p
                JOIN users u ON p.user_id = u.id
                WHERE u.username = %s
                LIMIT 1
                """,
                (username,),
            )
            row = cur.fetchone()
            if row:
                return row[0]

    return None


def get_valid_profile(user: User):
    """gets a users profile and check if complete"""

    profile_id = get_profile_id(user.username)

    if not profile_id:
        return None

    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT 
                        p.id, p.full_name, p.major, p.grad_year, p.linkedin_url, p.bio, p.image_url,
                        COALESCE(
                            json_agg(
                                json_build_object(
                                    'company', i.company, 
                                    'role', i.role, 
                                    'time_period', i.time_period
                                )
                            ) FILTER (WHERE i.id IS NOT NULL), 
                            '[]'
                        ) as internships
                    FROM profiles p
                    JOIN users u ON p.user_id = u.id
                    LEFT JOIN internships i ON p.id = i.profile_id
                    WHERE u.username = %s
                    GROUP BY p.id
                    """,
                    (user.username,),
                )
                row = cur.fetchone()

                if not row:
                    return None

                return Profile.from_db(row, row["internships"])

    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None


# helper for getting all profiles
def get_all_profiles():
    """gets a list of profiles"""

    try:
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    SELECT 
                        p.id, p.full_name, p.major, p.grad_year, p.linkedin_url, p.bio, p.image_url,
                        COALESCE(
                            json_agg(
                                json_build_object(
                                    'company', i.company, 
                                    'role', i.role, 
                                    'time_period', i.time_period
                                )
                            ) FILTER (WHERE i.id IS NOT NULL), 
                            '[]'
                        ) as internships
                    FROM profiles p
                    LEFT JOIN internships i ON p.id = i.profile_id
                    GROUP BY p.id
                    ORDER BY p.id DESC
                    """
                )
                rows = cur.fetchall()

                results = []
                for row in rows:
                    results.append(Profile.from_db(row, row["internships"]))

                return results

    except Exception as e:
        print(f"Error getting all profiles: {e}")
        return []


# profile WRITE functions


def update_profile(user: User, profile_update: ProfileUpdate):
    """updates a user profile in the db (including profile and internship)"""

    try:

        profile_id = get_profile_id(user.username)

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
                        (profile_id, user.username),
                    )

                update_data = profile_update.model_dump(exclude_unset=True)
                allowed_fields = [
                    "full_name",
                    "major",
                    "grad_year",
                    "linkedin_url",
                    "bio",
                    "image_url",
                ]

                set_clauses = []
                values = []

                for field in allowed_fields:
                    if field in update_data:
                        set_clauses.append(f"{field} = %s")
                        values.append(update_data[field])

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

                    # insert new internships (in bulk)
                    prev_internships = update_data.get("prev_internships")
                    if prev_internships:
                        params = [
                            (
                                profile_id,
                                internship["company"],
                                internship["role"],
                                internship["time_period"],
                            )
                            for internship in prev_internships
                        ]
                        cur.executemany(
                            """
                            INSERT INTO internships (profile_id, company, role, time_period)
                            VALUES (%s, %s, %s, %s)
                            """,
                            params,
                        )

                conn.commit()

            return get_valid_profile(user)

    except Exception as e:
        print(f"Database error in update_profile: {e}")
        return None
