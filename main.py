from dotenv import dotenv_values
from fastapi import FastAPI
from models import *
from repository import *
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
def _list_people():
    return ImageRepository.list()


