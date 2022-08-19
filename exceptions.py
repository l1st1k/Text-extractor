from typing import Type

from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import Field, BaseModel


__all__ = ('BaseAPIException', 'ImageNotFoundException', 'ImageAlreadyExistsException', 'get_exception_responses')


class BaseError(BaseModel):
    message: str = Field(description="Error message or description")
    identifier: str = Field(description="Unique identifier which this error references to")


class NotFoundError(BaseError):
    """The entity does not exist"""
    pass


class AlreadyExistsError(BaseError):
    """An entity being created already exists"""
    pass


class BaseAPIException(Exception):
    """Base error for custom API exceptions"""
    message = "Entity error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}


class ImageNotFoundException(BaseAPIException):
    """Error raised when an image does not exist"""
    message = "The image does not exist"
    model = NotFoundError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)


class ImageAlreadyExistsException(BaseAPIException):
    """Error raised when a image already exists"""
    message = "The image already exists"
    model = AlreadyExistsError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)


def get_exception_responses(*args: Type[BaseAPIException]) -> dict:
    """Given BaseAPIException classes, return a dict of responses used on FastAPI endpoint definition, with the format:
    {statuscode: schema, statuscode: schema, ...}"""
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
