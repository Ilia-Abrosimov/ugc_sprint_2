import datetime
from uuid import UUID

from maps.maps import UserReview
from pydantic import BaseModel, Field


class CreateReviewParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, который создает обзор')


class CreateReviewBody(BaseModel):
    film_id: UUID = Field(title='id фильма, для которого создается обзор')
    text: str = Field(title='Текст ревью')
    date: datetime.date = Field(title='Дата написания обзора')


class CreateReviewResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')


class GetUserReviewsParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, запрашивающего список своих обзоров')


class GetUserReviewsResponse(BaseModel):
    reviews: list[UserReview] = Field(title='Список фильмов с обзорами пользователя')


class GetUserReviewParams(BaseModel):
    review_id: str = Field(title='id обзора')


class GetUserReviewResponse(BaseModel):
    review: UserReview = Field(title='Обзор, созданный пользователем')


class UpdateReviewParams(CreateReviewParams):
    pass


class UpdateReviewBody(CreateReviewBody):
    pass


class UpdateReviewResponse(CreateReviewResponse):
    pass


class DeleteReviewParams(BaseModel):
    review_id: str = Field(title='id пользователя, который удаляет обзор')


class DeleteReviewResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')
