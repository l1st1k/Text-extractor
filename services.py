import base64
import logging
import os
from glob import glob
from uuid import uuid4

import pytesseract as tess
from PIL import Image

__all__ = ("get_uuid", "clear_pictures", "b64_to_image", "get_text_from_image")
tess.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
logging.basicConfig(level=logging.DEBUG)


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


def clear_pictures() -> None:
    """Deletes all local pictures"""
    removing_files = glob('./*.jpg') + glob('./*.png') + glob('./*.jpeg')
    for i in removing_files:
        os.remove(i)
    logging.info("ALL LOCAL PICTURES ARE CLEARED SUCCESSFULLY!")


def b64_to_image(title: str, b64_str: bytes) -> None:
    image_64_decode = base64.b64decode(b64_str)
    image_result = open(title, 'wb')  # create a writable image and write the decoding result
    image_result.write(image_64_decode)


def get_text_from_image(title: str, b64_str: bytes) -> str:
    b64_to_image(title, b64_str)
    return tess.image_to_string(Image.open(title))
