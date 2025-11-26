from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.auth import User
from ..util.auth import get_user
from ..util.profile import get_profile_id, update_profile_image
from ..util.images import ImageMiddleware, delete_object, put_object

# --- router ---
router = APIRouter(prefix="/images", tags=["Images"])

MAX_PROFILE_FILE_SIZE = 4.5 * 1024 * 1024  # 4.5 MB
PROFILE_BUCKET = "profiles"


# --- api endpoints ---
@router.put("/profile", status_code=status.HTTP_200_OK)
async def put_profile_image(
    user: Annotated[User, Depends(get_user)],
    buf: Annotated[BytesIO, Depends(ImageMiddleware(MAX_PROFILE_FILE_SIZE))],
):
    profile_id = get_profile_id(user.username)
    if profile_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile cannot be found"
        )

    url = await put_object(buf, PROFILE_BUCKET, str(profile_id))

    if not update_profile_image(profile_id, url):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update profile image"
        )


@router.delete("/profile", status_code=status.HTTP_200_OK)
async def delete_profile_image(user: Annotated[User, Depends(get_user)]):
    profile_id = get_profile_id(user.username)
    if profile_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile cannot be found"
        )

    await delete_object(PROFILE_BUCKET, str(profile_id))

    if not update_profile_image(profile_id, None):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete profile image"
        )
