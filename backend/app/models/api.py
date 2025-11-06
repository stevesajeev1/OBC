from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    next: str | None
    previous: str | None
    results: list[T]

    @classmethod
    def paginate(cls, results: list[T], page: int, pageSize: int, url: str):
        count = len(results)

        start = page * pageSize
        end = start + pageSize

        base_url = url.split("?")[0]
        next_url, prev_url = None, None
        if end < count:
            next_url = f"{base_url}?page={page + 1}&pageSize={pageSize}"
        if page > 0:
            prev_url = f"{base_url}?page={page - 1}&pageSize={pageSize}"

        response = {
            "count": count,
            "next": next_url,
            "previous": prev_url,
            "results": results[start:end],
        }
        return cls.model_validate(response)
