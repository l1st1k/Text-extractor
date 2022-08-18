from dotenv import dotenv_values
from fastapi import FastAPI
from mongoengine import connect

app = FastAPI()
config = dotenv_values(".env")
# connect(host=f"mongodb://{config['MONGO_USER']}:{config['MONGO_PASS']}@127.0.0.1:27017/{config['MONGO_DB']}?authSource=my_db")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
