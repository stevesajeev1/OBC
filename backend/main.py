from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from util.origin import get_allowed_origin

import os

VERCEL_ENV = os.getenv("VERCEL_ENV")

app = FastAPI()

allowed_origin = get_allowed_origin()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return allowed_origin


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
