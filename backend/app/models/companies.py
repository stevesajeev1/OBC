from pydantic import BaseModel


class Company(BaseModel):
    id: int = -1
    name: str
    url: str
    logo_url: str | None = None

    @classmethod
    def from_tuple(cls, tuple: tuple):
        return cls(id=tuple[0], name=tuple[1], url=tuple[2], logo_url=tuple[3])

    def to_tuple(self):
        return (self.name, self.url, self.logo_url)


class CompaniesResponse(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[Company]
