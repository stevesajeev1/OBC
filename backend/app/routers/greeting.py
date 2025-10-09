from fastapi import APIRouter

router = APIRouter(prefix="/greeting", tags=["greeting"])


@router.get("/")
async def greeting():
    return "Hello!"


@router.get("/{name}")
async def hello_name(name: str):
    return f"Hello, {name}!"
