from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import (auth, companies, cron, favorites, greeting, listings,
                      users)
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

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(cron.router)
app.include_router(favorites.router)
app.include_router(greeting.router)
app.include_router(listings.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return "Hello, world!"
