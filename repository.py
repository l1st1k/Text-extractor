from __future__ import annotations

import base64

from fastapi import UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

from database import collection
from exceptions import *
from models import *
from services import *

__all__ = ("ImageRepository",)


class ImageRepository:
    @staticmethod
    def list() -> ImagesRead:
        """Retrieve all the available images"""
        # Deleting previous pictures
        clear_pictures()

        # Database logic
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

            # Creating the instance
            encoded_string: bytes = base64.b64encode(file.file.read())
            data = ImageCreate(image_id=str(get_uuid()))
            data.b64_encoded_string = encoded_string
            data.title = file.filename

            # Text extracting logic
            data.text = get_text_from_image(title=data.title, b64_str=bytes(data.b64_encoded_string))

            # Deleting previous pictures
            clear_pictures()

            # Database logic
            document = data.dict()
            collection.insert_one(document)

            # Response
            response = JSONResponse(
                content={"message": f"Your image uploaded successfully! If you want to change title "
                                    f"from '{data.title}' to another or add some description for that "
                                    f"picture, you can update information with the corresponding 'Update'"
                                    f" method!",
                         "id": data.image_id},
                status_code=status.HTTP_201_CREATED)
        except TypeError:
            response = JSONResponse(content={"message": "Picture should be in jpg/jpeg/png format!"},
                                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        return response

    @staticmethod
    def update(image_id: str, update: ImageUpdate) -> ImageRead | JSONResponse:
        """Update an image by giving only the fields to update"""
        # Deleting previous pictures
        clear_pictures()
        try:
            document = collection.find_one({"image_id": image_id})
            if not document:
                raise ImageNotFoundException(image_id)
            update_document = update.dict()
            collection.update_one({"image_id": image_id}, {"$set": update_document})
            document = collection.find_one({"image_id": image_id})
            response = ImageRead(**document)
        except ImageNotFoundException:
            response = JSONResponse(content={"message": "There is no image with that ID!"},
                                    status_code=status.HTTP_404_NOT_FOUND)
        return response

    @staticmethod
    def delete(image_id: str) -> JSONResponse:
        """Deletes a single Image by its unique id"""
        # Deleting previous pictures
        clear_pictures()

        try:
            document = collection.find_one({"image_id": image_id})
            if not document:
                raise ImageNotFoundException(image_id)
            collection.delete_one({"image_id": image_id})
            response = JSONResponse(content={"message": "Successfully deleted!"}, status_code=status.HTTP_200_OK)
        except ImageNotFoundException:
            response = JSONResponse(content={"message": "There is no image with that ID!"},
                                    status_code=status.HTTP_404_NOT_FOUND)
        return response

    @staticmethod
    def find(text_to_find: str) -> ImagesRead:
        """Finds images with the corresponding text on them"""
        cursor = collection.find({"text": {"$regex": text_to_find, "$options": "i"}})
        return [ImageRead(**document) for document in cursor]
