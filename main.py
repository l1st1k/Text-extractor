from dotenv import dotenv_values
from fastapi import FastAPI
from models import *
from repository import *
from exceptions import *
from mongoengine import connect

app = FastAPI()
config = dotenv_values(".env")
# connect(host=f"mongodb://{config['MONGO_USER']}:{config['MONGO_PASS']}@127.0.0.1:27017/{config['MONGO_DB']}?authSource=my_db")


@app.get("/")
async def root():
    return {"message": "Hello World"}


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

