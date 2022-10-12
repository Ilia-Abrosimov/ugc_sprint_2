"""
Модель данных, загружаемых в хранилище.

"""

import uuid

from pydantic import BaseModel, Field


def get_id() -> str:
    return str(uuid.uuid4())


class User(BaseModel):
    id: str = Field(title='User id', default_factory=get_id)


class Film(BaseModel):
    id: str = Field(title='Film id', default_factory=get_id)


class UserAction(BaseModel):
    user_id: str = Field(title='User id')
    film_id: str = Field(title='Film id')
    like: int = Field(title='Like or dislike')
