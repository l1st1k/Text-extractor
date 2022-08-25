from fastapi import FastAPI, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

from exceptions import *
from models import *
from repository import *

app = FastAPI()


@app.get(
    "/images",
    response_model=ImagesRead,
    description="List all the images",
    tags=["Images"]
)
def _list_images():
    return ImageRepository.list()


@app.get(
    "/image/{image_id}",
    response_class=FileResponse,
    description="Get a single picture by its unique ID",
    responses=get_exception_responses(ImageNotFoundException),
    status_code=status.HTTP_200_OK,
    tags=["Image"]
)
def _get_image(image_id: str):
    return ImageRepository.get(image_id=image_id)


@app.post(
    "/image",
    response_class=JSONResponse,
    description="Upload a new image",
    status_code=status.HTTP_201_CREATED,
    tags=["Image"]
)
def _upload_image(file: UploadFile):
    return ImageRepository.create(file=file)


@app.patch(
    "/image/{image_id}",
    response_class=JSONResponse or ImageRead,
    description="Update title/description for the image",
    status_code=status.HTTP_200_OK,
    tags=["Image"]
)
def _update_image(image_id: str, update: ImageUpdate):
    return ImageRepository.update(image_id=image_id, update=update)


@app.delete(
    "/image/{image_id}",
    response_class=JSONResponse,
    description="Delete the image",
    status_code=status.HTTP_200_OK,
    tags=["Image"]
)
def _delete_image(image_id: str):
    return ImageRepository.delete(image_id=image_id)
