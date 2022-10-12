"""
Модель данных, загружаемых в хранилище.

"""

import random

from etl.src.models.models import get_new_id
from pydantic import BaseModel, Field


def get_random_num() -> int:
    return random.randint(1, 1000)


class UserHistory(BaseModel):
    id: str = Field(title='uuid', default_factory=get_new_id)
    user_id: str = Field(title='User id', default_factory=get_new_id)
    film_id: str = Field(title='Film id', default_factory=get_new_id)
    viewed_frame: int = Field(title='Film viewed frame', default_factory=get_random_num)
