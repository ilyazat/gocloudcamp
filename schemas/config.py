from pydantic import BaseModel


class Config(BaseModel):
    service: str
    data: list[dict[str, str]]
    used_by: list[str] = []


class ConfigToDB(Config):
    version: int
