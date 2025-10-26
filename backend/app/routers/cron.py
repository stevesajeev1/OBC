import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Header, HTTPException, status

from ..util.cron import assign_logos, get_listings, insert_listings

load_dotenv()

CRON_SECRET = os.getenv("CRON_SECRET")

router = APIRouter(prefix="/cron", tags=["cron"])


@router.get("/", status_code=status.HTTP_200_OK)
async def scrape(Authorization: Annotated[str, Header()]):
    if Authorization != f"Bearer {CRON_SECRET}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    # Get listings
    listings = get_listings()
    # Assign company logos to listings
    assign_logos(listings)
    # Insert listings into DB
    insert_listings(listings)
