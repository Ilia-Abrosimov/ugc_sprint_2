"""
Модели данных, перегружаемых из OLTP в OLAP.

"""

import uuid

from pydantic import BaseModel, Field


def get_new_id() -> str:
    return str(uuid.uuid4())


class UserHistory(BaseModel):
    id: str = Field(title='uuid', default_factory=get_new_id)
    user_id: str = Field(title='User id')
    film_id: str = Field(title='Film id')
    viewed_frame: int = Field(title='Film viewed frame')
