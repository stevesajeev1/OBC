from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import greeting
from .util.origin import get_allowed_origin


app = FastAPI()

allowed_origin = get_allowed_origin()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(greeting.router)


@app.get("/")
async def root():
    return "Hello, world!"
