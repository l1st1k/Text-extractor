from fastapi import FastAPI, status, UploadFile
from fastapi.responses import JSONResponse

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
    response_model=ImageRead,
    description="Get a single image by its unique ID",
    responses=get_exception_responses(ImageNotFoundException),
    tags=["image"]
)
def _get_image(image_id: str):
    return ImageRepository.get(image_id=image_id)


@app.post(
    "/upload_image",
    description="Upload a new image",
    status_code=status.HTTP_201_CREATED,
    tags=["image"]
)
def _upload_image(file: UploadFile):
    try:
        # Type check
        if file and (file.content_type not in ('image/jpeg', 'image/png', 'image/jpg')):
            raise TypeError
        encoded_string: bytes = base64.b64encode(file.file.read())
        data = ImageCreate(image_id=get_uuid())
        data.b64_encoded_string = encoded_string
        data.title = file.filename
        print(data.image_id)
        response = JSONResponse(content={"message": f"Your image uploaded successfully! If you want to change title "
                                                    f"from '{data.title}' to another or add some description for that "
                                                    f"picture, you can update information with the corresponding Update"
                                                    f" method!",
                                         "id": data.image_id},
                                status_code=status.HTTP_201_CREATED)
    except TypeError:
        response = JSONResponse(content={"message": "Picture should be in jpg/jpeg/png format!"},
                                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    return response




