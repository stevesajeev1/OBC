from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .util.origin import get_allowed_origin
from .util.prisma import Prisma
from .routers import greeting


@asynccontextmanager
async def lifespan(_):
    prisma = Prisma()
    await prisma.connect()
    yield
    await prisma.disconnect()


app = FastAPI(lifespan=lifespan)

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
