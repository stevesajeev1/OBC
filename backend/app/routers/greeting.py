import os

import psycopg
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

router = APIRouter(prefix="/greeting", tags=["greeting"])


@router.get("/", status_code=status.HTTP_200_OK)
async def greeting():
    return "Hello!"


@router.get("/names", status_code=status.HTTP_200_OK)
async def greet_names():
    if DATABASE_URL is None:
        raise HTTPException(status_code=500, detail="Could not connect to DB")

    try:
        async with await psycopg.AsyncConnection.connect(DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT name FROM test;")
                rows = await cur.fetchall()

        names = [row[0] for row in rows]
        return f"Hello, {', '.join(names)}!"
    except Exception:
        raise HTTPException(status_code=500, detail="Could not connect to DB")


@router.get("/{name}", status_code=status.HTTP_200_OK)
async def greet_name(name: str):
    return f"Hello, {name}!"
