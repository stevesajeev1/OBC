from fastapi import APIRouter, Depends, status
from typing import Annotated
from ..models.auth import User
from ..util.auth import get_user
from ..util.images import ImageMiddleware, put_object, delete_object
from io import BytesIO

# --- router ---
router = APIRouter(prefix="/images", tags=["Images"])

MAX_PROFILE_FILE_SIZE = 4.5 * 1024 * 1024 # 4.5 MB
PROFILE_BUCKET = "profiles"

# --- api endpoints ---
@router.put("/profile", status_code=status.HTTP_200_OK)
async def put_profile_image(user: Annotated[User, Depends(get_user)], buf: Annotated[BytesIO, Depends(ImageMiddleware(MAX_PROFILE_FILE_SIZE))]):
    assert user.id is not None

    # TODO: Replace user ID with profile ID
    return await put_object(buf, PROFILE_BUCKET, str(user.id))
    # TODO: Update Profile object in DB

@router.delete("/profile", status_code=status.HTTP_200_OK)
async def delete_profile_image(user: Annotated[User, Depends(get_user)]):
    assert user.id is not None

    # TODO: Replace user ID with profile ID
    await delete_object(PROFILE_BUCKET, str(user.id))
    # TODO: Update Profile object in DB