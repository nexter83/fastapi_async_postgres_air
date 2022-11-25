from pydantic import BaseModel
from enum import Enum


class Roles(str, Enum):
    ADMIN = 'admin'
    USER = 'user'


class BaseUser(BaseModel):
    username: str
    email: str
    user_role: Roles = None


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    type_toke: str = "bearer"

