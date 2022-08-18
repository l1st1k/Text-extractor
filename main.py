from fastapi import FastAPI
from dotenv import dotenv_values

app = FastAPI()
config = dotenv_values(".env")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
