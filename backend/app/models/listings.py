from pydantic import BaseModel

from .cron import Listing


class ListingsResponse(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[Listing]
