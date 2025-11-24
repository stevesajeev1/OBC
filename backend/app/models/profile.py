from typing import Any, Optional

from pydantic import BaseModel


class Internship(BaseModel):
    """structure for past internship"""

    company: str
    role: str
    time_period: list[str]  # ex. Summer 2025


class Profile(BaseModel):
    """fields that are allowed to be updated by user (all optional)"""

    full_name: Optional[str] = None
    major: Optional[str] = None
    grad_year: Optional[int] = None  # Class of 2028
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    prev_internships: list[Internship] = []

    @classmethod
    def from_db(
        cls, profile_row: dict[str, Any], internship_rows: list[dict[str, Any]] | None
    ):
        """classmethod to create profile instance from db row"""
        internships: list[Internship] | None = None
        if internship_rows:
            internships = []
            for row in internship_rows:
                internships.append(
                    Internship(
                        company=row.get("company"),
                        role=row.get("role"),
                        time_period=row.get("time_period"),
                    )
                )

        return cls(
            full_name=profile_row.get("full_name"),
            major=profile_row.get("major"),
            grad_year=profile_row.get("grad_year"),
            linkedin_url=profile_row.get("linkedin_url"),
            bio=profile_row.get("bio"),
            image_url=profile_row.get("image_url"),
            prev_internships=internships,
        )


class ProfileUpdate(BaseModel):
    """fields that can be updated"""

    full_name: Optional[str] = None
    major: Optional[str] = None
    grad_year: Optional[int] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    prev_internships: Optional[list[Internship]] = None
    image_url: Optional[str] = None
