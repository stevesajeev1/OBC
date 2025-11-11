from pydantic import BaseModel


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
    prev_internships: list[Internship] | None = None


class ProfileUpdate(BaseModel):
    """fields that can be updated"""

    full_name: str | None = None
    major: str | None = None
    grad_year: int | None = None
    linkedin_link: str | None = None
    bio: str | None = None
    prev_internships: list[Internship] | None = None
