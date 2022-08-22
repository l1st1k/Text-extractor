from fastapi.responses import JSONResponse
from database import collection
from models import *
from exceptions import *
from services import *

__all__ = ("ImageRepository",)


class ImageRepository:
    @staticmethod
    def get(image_id: str) -> ImageRead:
        """Retrieve a single Image by its unique id"""
        document = collection.find_one({"_id": image_id})
        if not document:
            raise ImageNotFoundException(image_id)
        return ImageRead(**document)

    @staticmethod
    def list() -> ImagesRead:
        """Retrieve all the available images"""
        cursor = collection.find()
        return [ImagesRead(**document) for document in cursor]

    @staticmethod
    def create(create: ImageCreate) -> ImageRead:
        """Create an image and return its Read object"""
        document = create.dict()
        document["_id"] = get_uuid()
        result = collection.insert_one(document)
        return ImageRepository.get(result.inserted_id)

    @staticmethod
    def update(image_id: str, update: ImageUpdate) -> ImageRead:

        return ImageRead(**updated_document)

    @staticmethod
    def delete(image_id: str) -> JSONResponse:

        return response
