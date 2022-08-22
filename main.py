from fastapi import FastAPI, status
from models import *
from repository import *
from exceptions import *

app = FastAPI()


@app.get(
    "/images",
    response_model=ImagesRead,
    description="List all the images",
    tags=["image"]
)
def _list_images():
    return ImageRepository.list()


@app.get(
    "/image/{image_id}",
    response_model=ImageRead,
    description="Get a single image by its unique ID",
    responses=get_exception_responses(ImageNotFoundException),
    tags=["image"]
)
def _get_image(image_id: str):
    return ImageRepository.get(image_id=image_id)


@app.post(
    "/image",
    description="Create a new image",
    response_model=ImageRead,
    status_code=status.HTTP_201_CREATED,
    responses=get_exception_responses(ImageAlreadyExistsException),
    tags=["image"]
)
def _create_image(create: ImageCreate):
    return ImageRepository.create(create)

