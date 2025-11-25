import importlib
import pkgutil

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routers
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

included_routers = []
for _, module_name, _ in pkgutil.iter_modules(routers.__path__):
    module = importlib.import_module(f"{routers.__name__}.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)
        included_routers.append(module_name)
print(f"Included routers from: {', '.join(included_routers)}")


@app.get("/")
async def root():
    return "Hello, world!"
