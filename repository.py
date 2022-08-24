import base64
import os

from fastapi.responses import FileResponse, JSONResponse
from fastapi import status

from database import collection
from models import *
from fastapi import UploadFile
from exceptions import *
from services import *

__all__ = ("ImageRepository",)


class ImageRepository:
    @staticmethod
    def list() -> ImagesRead:
        """Retrieve all the available images"""
        cursor = collection.find()
        return [ImageRead(**document) for document in cursor]

    @staticmethod
    def get(image_id: str) -> FileResponse:
        """Retrieve a single Image by its unique id"""
        # Deleting previous pictures
        clear_pictures()

        # Taking document from DB
        document = collection.find_one({"image_id": image_id})
        if not document:
            raise ImageNotFoundException(image_id)
        b64_str = document['b64_encoded_string']
        title = str(document['title'])

        # Converting base64 into image
        b64_to_image(title, b64_str)
        return FileResponse(title)

    @staticmethod
    def create(file: UploadFile) -> JSONResponse:
        """Upload a picture and return its id"""
        try:
            # Type check
            if file and (file.content_type not in ('image/jpeg', 'image/png', 'image/jpg')):
                raise TypeError
            encoded_string: bytes = base64.b64encode(file.file.read())
            data = ImageCreate(image_id=str(get_uuid()))
            data.b64_encoded_string = encoded_string
            data.title = file.filename
            # text logic

            # database logic
            document = data.dict()
            collection.insert_one(document)
            # response
            response = JSONResponse(
                content={"message": f"Your image uploaded successfully! If you want to change title "
                                    f"from '{data.title}' to another or add some description for that "
                                    f"picture, you can update information with the corresponding Update"
                                    f" method!",
                         "id": data.image_id},
                status_code=status.HTTP_201_CREATED)
        except TypeError:
            response = JSONResponse(content={"message": "Picture should be in jpg/jpeg/png format!"},
                                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        return response

    # @staticmethod
    # def update(image_id: str, update: ImageUpdate) -> ImageRead:
    #
    #     return ImageRead(**updated_document)
    #
    # @staticmethod
    # def delete(image_id: str) -> JSONResponse:
    #
    #     return response
