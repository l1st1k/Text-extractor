import pydantic

__all__ = ("mongo_settings",)


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"


class MongoSettings(BaseSettings):
    uri: str = "mongodb://127.0.0.1:27017"
    database: str = "main_db"
    collection: str = "image_test"

    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"


mongo_settings = MongoSettings()
