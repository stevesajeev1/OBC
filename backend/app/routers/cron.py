import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Header, HTTPException

load_dotenv()

CRON_SECRET = os.getenv("CRON_SECRET")

router = APIRouter(prefix="/cron", tags=["cron"])


@router.get("/")
async def scrape(Authorization: Annotated[str, Header()]):
    if Authorization != f"Bearer {CRON_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Do logic here

    return "Hello, world!"
