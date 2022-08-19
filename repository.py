from fastapi.responses import JSONResponse

from models import *

__all__ = ("ImageRepository",)


class ImageRepository:
    @staticmethod
    def get(image_id: str) -> ImageRead:

        return ImageRead(**document)

    @staticmethod
    def list(image_id: str) -> ImagesRead:

        return [ImagesRead(**document) for document in cursor]

    @staticmethod
    def create(create: ImageCreate) -> ImageRead:

        return ImageRepository.get(result.inserted_id)

    @staticmethod
    def update(image_id: str, update: ImageUpdate) -> ImageRead:

        return ImageRead(**updated_document)

    @staticmethod
    def delete(image_id: str) -> JSONResponse:

        return response
