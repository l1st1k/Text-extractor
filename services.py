import base64
import os
from glob import glob
from uuid import uuid4

__all__ = ("get_uuid", "clear_pictures", "b64_to_image")


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


def clear_pictures() -> None:
    """Deletes all local pictures"""
    removing_files = glob('./*.jpg') + glob('./*.png') + glob('./*.jpeg')
    for i in removing_files:
        os.remove(i)
    print("ALL LOCAL PICTURES ARE CLEARED SUCCESSFULLY!")


def b64_to_image(title: str, b64_str: str) -> None:
    image_64_decode = base64.b64decode(b64_str)
    image_result = open(title, 'wb')  # create a writable image and write the decoding result
    image_result.write(image_64_decode)
