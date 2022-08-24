from fastapi import FastAPI, status, UploadFile
from fastapi.responses import JSONResponse, FileResponse

from models import *
from repository import *
from exceptions import *
from services import *
from bson.binary import Binary
import gridfs
import base64
from database import client

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
    response_class=FileResponse,
    description="Get a single picture by its unique ID",
    responses=get_exception_responses(ImageNotFoundException),
    tags=["image"]
)
def _get_image(image_id: str):
    return ImageRepository.get(image_id=image_id)


@app.post(
    "/upload_image",
    response_class=JSONResponse,
    description="Upload a new image",
    status_code=status.HTTP_201_CREATED,
    tags=["image"]
)
def _upload_image(file: UploadFile):
    return ImageRepository.create(file=file)
