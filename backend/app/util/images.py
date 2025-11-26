from io import BytesIO

from fastapi import HTTPException, UploadFile, status
from PIL import Image
from vercel.blob import AsyncBlobClient

ALLOWED_IMAGE_TYPES = set(["image/jpeg", "image/jpg", "image/png", "image/webp"])


class ImageMiddleware:
    def __init__(self, max_file_size: float):
        self.max_file_size = max_file_size

    def __call__(self, file: UploadFile):
        # check content type
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is not an image",
            )

        # check if image is malformed
        try:
            with Image.open(file.file) as im:
                im.verify()
            with Image.open(file.file) as im:
                buf = BytesIO()
                im.save(buf, "WEBP")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file is malformed",
            )

        # check file size
        if buf.getbuffer().nbytes > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size too large",
            )

        buf.seek(0)
        return buf


async def put_object(object: BytesIO, bucket: str, key: str) -> str:
    path = f"{bucket}/{key}.webp"

    client = AsyncBlobClient()
    blob = await client.put(path, object, access="public", overwrite=True)
    return blob.url


async def delete_object(bucket: str, key: str):
    path = f"{bucket}/{key}.webp"

    client = AsyncBlobClient()
    await client.delete(path)
