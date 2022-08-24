from fastapi import FastAPI, status, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pydantic.typing import NoneType

from models import *
from repository import *
from exceptions import *
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
    response_model=ImageRead or JSONResponse,
    status_code=status.HTTP_201_CREATED,
    responses=get_exception_responses(ImageAlreadyExistsException),
    tags=["image"]
)
def _create_image(create: ImageCreate = DEFAULT_IMAGE_MODEL,
                  file: UploadFile = File(description="The picture by itself", default=None)):
    try:
        # Type check
        # print(file.filename, file.content_type)
        # print(file.content_type == "image/jpeg")
        # print(file.content_type not in ('image/jpeg', 'image/png', 'image/jpg'))
        if file and (file.content_type not in ('image/jpeg', 'image/png', 'image/jpg')):
            print(True)
            raise TypeError
        print(create.b64_encoded_string)
        print(create.title)
        # User should send only 1 of 2 parameters(picture or b64_string of his picture)
        if not (file or create.b64_encoded_string):
            raise ValueError
        if file and create.b64_encoded_string:
            raise ValueError

        encoded_string: bytes = base64.b64encode(file.file.read())
        # data = ImageRead()
        # data.b64_encoded_string = encoded_string
        response = JSONResponse(content={"message": "HIQ"})
    except TypeError:
        response = JSONResponse(content={"message": "Picture should be in jpg/jpeg/png format!"},
                                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    except ValueError:
        response = JSONResponse(content={"message": "You should send 1 of 2 parameters "
                                                    "(b64_encoded_string or picture by itself)"},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return response

