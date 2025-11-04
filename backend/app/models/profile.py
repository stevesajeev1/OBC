from pydantic import BaseModel, HttpUrl

class Internship(BaseModel):
    """structure for past internship"""
    company: str
    role: str
    time_period: str # ex. Summer 2025

class ProfileBase(BaseModel):
    """fields that are allowed to be updated by user"""
    full_name: str
    major: str
    grad_year: int # Class of 2028
    linkedin_link: HttpUrl
    bio: str | None = None
    prev_internships: list[Internship] | None = None

    class Config:
        orm_mode = True

class ProfileUpdate(BaseModel):
    """fields that can be updated"""
    full_name: str | None = None
    major: str | None = None
    grad_year: int | None = None
    linkedin_link: HttpUrl | None = None
    bio: str | None = None
    prev_internships: list[Internship] | None = None

class ProfilePublic(ProfileBase):
    """public facing"""
    username: str

