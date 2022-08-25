import pydantic
from dotenv import dotenv_values

__all__ = ("mongo_settings",)
config = dotenv_values(".env")


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"


class MongoSettings(BaseSettings):
    uri: str = f"mongodb://{config['MONGO_USER']}:{config['MONGO_PASS']}" \
               f"@127.0.0.1:27017/{config['MONGO_DB']}?authSource=admin"
    database: str = "main_db"
    collection: str = "image_test"

    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"


mongo_settings = MongoSettings()
