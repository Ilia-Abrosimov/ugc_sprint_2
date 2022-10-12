"""
Модель данных, загружаемых в хранилище.

"""

import random

from pydantic import BaseModel, Field
from src.settings import settings


def get_user_id() -> int:
    return random.randint(1, settings.user_num)


def get_film_id() -> int:
    return random.randint(1, settings.films_num)


def get_viewed_frame() -> int:
    return random.randint(1, settings.films_max_length)


class UserHistory(BaseModel):
    user_id: int = Field(title='User id', default_factory=get_user_id)
    film_id: int = Field(title='Film id', default_factory=get_film_id)
    viewed_frame: int = Field(title='Film viewed frame', default_factory=get_viewed_frame)
