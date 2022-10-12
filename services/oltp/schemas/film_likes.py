from enum import IntEnum
from uuid import UUID

from maps.maps import UserLikes
from pydantic import BaseModel, Field


class LikeType(IntEnum):
    like = 1
    dislike = 0


class LikeFilmParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, который ставит фильму оценку')


class LikeFilmBody(BaseModel):
    film_id: UUID = Field(title='id фильма, которому ставится оценка')
    value: LikeType = Field(title='Оценка фильма')


class LikeFilmResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')


class GetUserLikesParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, запрашивающего список своих оценок фильмам')


class GetUserLikesResponse(BaseModel):
    films: list[UserLikes] = Field(title='Список фильмов с оценками пользователя')


class UpdateLikeParams(LikeFilmParams):
    pass


class UpdateLikeBody(LikeFilmBody):
    pass


class UpdateLikeResponse(LikeFilmResponse):
    pass


class DeleteFilmLikeParams(BaseModel):
    like_id: str = Field(title='id удаляемой оценки')


class DeleteFilmLikeResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')
