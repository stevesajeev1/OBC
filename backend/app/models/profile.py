from pydantic import BaseModel
from typing import Any


class Internship(BaseModel):
    """structure for past internship"""

    company: str
    role: str
    time_period: list[str]  # ex. Summer 2025


class Profile(BaseModel):
    """fields that are allowed to be updated by user"""

    full_name: str
    major: str
    grad_year: int  # Class of 2028
    linkedin_link: str
    bio: str | None = None
    image_url: str | None = None
    prev_internships: list[Internship] = []


    @classmethod
    def from_db(cls, profile_row: dict[str, Any], internship_rows: list[dict[str, Any]]):
        """classmethod to create profile instance from db row"""
        internships = []
        if internship_rows:
            for row in internship_rows:
                internships.append(Internship(
                    company = row['company'],
                    role = row['role'],
                    time_period = row['time_period']
                ))

        return cls(
            full_name=profile_row['full_name'],
            major=profile_row['major'],
            grad_year=profile_row['grad_year'],
            linkedin_link=profile_row['linkedin_url'], 
            bio=profile_row['bio'],
            image_url=profile_row.get('image_url'),
            prev_internships=internships
        )

class ProfileUpdate(BaseModel):
    """fields that can be updated"""

    full_name: str | None = None
    major: str | None = None
    grad_year: int | None = None
    linkedin_link: str | None = None
    bio: str | None = None
    prev_internships: list[Internship] | None = None
