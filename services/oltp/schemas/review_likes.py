from enum import IntEnum
from uuid import UUID

from maps.maps import UserReviewLikes
from pydantic import BaseModel, Field


class LikeType(IntEnum):
    like = 1
    dislike = 0


class LikeReviewParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, который ставит обзору оценку')


class LikeReviewBody(BaseModel):
    review_id: UUID = Field(title='id обзора, которому ставится оценка')
    value: LikeType = Field(title='Оценка обзору')


class LikeReviewResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')


class GetUserLikesParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, запрашивающего список своих оценок обзорам')


class GetUserLikesResponse(BaseModel):
    reviews: list[UserReviewLikes] = Field(title='Список обзоров с оценками пользователя')


class UpdateReviewLikeParams(LikeReviewParams):
    pass


class UpdateReviewLikeBody(LikeReviewBody):
    pass


class UpdateReviewLikeResponse(LikeReviewResponse):
    pass


class DeleteReviewLikeParams(BaseModel):
    like_id: str = Field(title='id удаляемой оценки')


class DeleteReviewLikeResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')
