from fastapi import APIRouter, Request, status

from ..models.companies import CompaniesResponse
from ..util.companies import get_companies_from_db

# --- router ---
router = APIRouter(prefix="/companies", tags=["Companies"])


# --- api endpoints ---
@router.get("/", response_model=CompaniesResponse, status_code=status.HTTP_200_OK)
def get_listings(request: Request, page: int = 0, pageSize: int = 100):
    companies = get_companies_from_db()
    count = len(companies)

    start = page * pageSize
    end = start + pageSize

    base_url = str(request.url).split("?")[0]
    next_url, prev_url = None, None
    if end < count:
        next_url = f"{base_url}?page={page + 1}&pageSize={pageSize}"
    if page > 0:
        prev_url = f"{base_url}?page={page - 1}&pageSize={pageSize}"

    response = {
        "count": count,
        "next": next_url,
        "previous": prev_url,
        "results": companies[start:end],
    }
    return CompaniesResponse.model_validate(response)
