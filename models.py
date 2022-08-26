from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ("ImageUpdate", "ImageCreate", "ImageRead", "ImagesRead",)


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
    title: Optional[str] = ImageFields.title
    description: Optional[str] = ImageFields.description


class ImageCreate(BaseModel):
    """Body of Image POST requests"""
    image_id: str = ImageFields.image_id
    title: str = ImageFields.title
    b64_encoded_string: bytes = ImageFields.b64_encoded_string
    text: str = ImageFields.text


class ImageRead(BaseModel):
    """Body of Image GET response"""
    image_id: str = ImageFields.image_id
    title: str = ImageFields.title
    description: str = ImageFields.description
    text: str = ImageFields.text


ImagesRead = List[ImageRead]
