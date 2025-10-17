import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Header, HTTPException, status

load_dotenv()

CRON_SECRET = os.getenv("CRON_SECRET")

router = APIRouter(prefix="/cron", tags=["cron"])


@router.get("/", status_code=status.HTTP_200_OK)
async def scrape(Authorization: Annotated[str, Header()]):
    if Authorization != f"Bearer {CRON_SECRET}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    # Do logic here

    return "Hello, world!"
