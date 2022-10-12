from uuid import UUID

from pydantic import BaseModel


class MainModel(BaseModel):
    user_id: UUID
    film_id: UUID


class FilmProgressBody(MainModel):
    progress: int


class FilmProgressResponse(BaseModel):
    pass
