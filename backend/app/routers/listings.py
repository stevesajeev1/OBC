from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..models.auth import User
from ..models.listings import ListingsResponse
from ..util.auth import get_user
from ..util.listings import delete_listing_in_db, get_listings_from_db

# --- router ---
router = APIRouter(prefix="/listings", tags=["Listings"])


# --- api endpoints ---
@router.get("/", response_model=ListingsResponse, status_code=status.HTTP_200_OK)
def get_listings(request: Request, page: int = 0, pageSize: int = 100):
    listings = get_listings_from_db()
    count = len(listings)

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
        "results": listings[start:end],
    }
    return ListingsResponse.model_validate(response)


@router.delete("/{listing_id}", status_code=status.HTTP_200_OK)
def delete_listing(listing_id: UUID, user: Annotated[User, Depends(get_user)]):
    if not user.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Need to be administrator to delete listings",
        )

    if not delete_listing_in_db(listing_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete listing with id {listing_id}",
        )
