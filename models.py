from pydantic import BaseModel
from typing import Optional


class VersionData(BaseModel):
    version: str


class Hwid(BaseModel):
    hwid: str


class Key(BaseModel):
    key: str
    hwid: str
