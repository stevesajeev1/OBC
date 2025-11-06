from fastapi import APIRouter, Request, status

from ..models.api import PaginatedResponse
from ..models.companies import Company
from ..util.companies import get_companies_from_db

# --- router ---
router = APIRouter(prefix="/companies", tags=["Companies"])


# --- api endpoints ---
@router.get(
    "/", response_model=PaginatedResponse[Company], status_code=status.HTTP_200_OK
)
def get_companies(request: Request, page: int = 0, pageSize: int = 100):
    companies = get_companies_from_db()
    return PaginatedResponse.paginate(companies, page, pageSize, str(request.url))
