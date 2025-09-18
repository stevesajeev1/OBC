from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

allowed_origin = os.getenv("FRONTEND_URL")
app.add_middleware(
    CORSMiddleware, allowed_origin, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def read_root():
    return "Hello, world!"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
