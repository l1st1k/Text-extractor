from pydantic import BaseModel, Field
from bson.binary import Binary
from fastapi import UploadFile, File
from typing import Optional, List
import pydantic


__all__ = ("ImageUpdate", "ImageCreate", "ImageRead", "ImagesRead", "DEFAULT_IMAGE_MODEL")


class ImageFields:
    image_id = Field(
        description="Unique identifier of this image in the database",
        example="3422b448-2460-4fd2-9183-8000de6f8343",
        min_length=36,
        max_length=36
    )
    b64_encoded_string = Field(
        description="Picture in bytes",
        default=None
    )
    title = Field(
        description="The title for the picture",
        default="Unnamed picture =(",
        example="Lecture #3"
    )
    description = Field(
        description="The description of the picture",
        default="Empty description =(",
        example="The lecture was about AWS services (SES, S3)"
    )
    text = Field(
        description="Text from the picture",
        default="There is no text on this image",
        example="AWS services (SES, S3)"
    )


class ImageUpdate(BaseModel):
    """Body of Image PATCH requests"""
    b64_encoded_string: Optional[bytes] = ImageFields.b64_encoded_string
    title: Optional[str] = ImageFields.title
    description: Optional[str] = ImageFields.description

    # TEXT EXTRACTING LOGIC (will be soon) TODO logic for text


class ImageCreate(ImageUpdate):
    """Body of Image POST requests"""
    title: str = ImageFields.title


class ImageRead(ImageUpdate):
    """Body of Image GET and POST responses"""
    image_id: str = ImageFields.image_id
    title: str = ImageFields.title
    description: str = ImageFields.description

    @pydantic.root_validator(pre=True)
    def _set_image_id(cls, data):
        """Swap the field _id to image_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "image_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["image_id"] = document_id
        return data


ImagesRead = List[ImageRead]

DEFAULT_IMAGE_MODEL = ImageCreate(
    b64_encoded_string=None,
    title="Unnamed picture =(",
    description="Empty description =("
)
