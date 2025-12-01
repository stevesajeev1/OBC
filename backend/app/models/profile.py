from typing import Any, Optional

from pydantic import BaseModel, Field


class Internship(BaseModel):
    """structure for past internship"""

    company: str
    role: str
    time_period: list[str] = []  # ex. Summer 2025


class Profile(BaseModel):
    """fields that are allowed to be updated by user (all optional)"""

    full_name: Optional[str] = None
    major: Optional[str] = None
    grad_year: Optional[int] = None  # Class of 2028
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    prev_internships: list[Internship] = []
    public: bool = False

    @classmethod
    def from_db(
        cls, profile_row: dict[str, Any], internship_rows: list[dict[str, Any]] | None
    ):
        """classmethod to create profile instance from db row"""
        internships: list[Internship] = []
        if internship_rows:
            internships = []
            for row in internship_rows:
                internships.append(
                    Internship(
                        company=row["company"],
                        role=row["role"],
                        time_period=row["time_period"],
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
            public=profile_row.get("public", False),
        )


class ProfileUpdate(BaseModel):
    """fields that can be updated"""

    full_name: Optional[str] = None
    major: Optional[str] = None
    grad_year: Optional[int] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None
    prev_internships: Optional[list[Internship]] = None
    public: Optional[bool] = Field(
        default=None,
        description="A profile can only be marked as public if it has a full name set.",
    )
