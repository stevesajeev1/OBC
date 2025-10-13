from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, cron, greeting
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

app.include_router(cron.router)
app.include_router(greeting.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return "Hello, world!"
