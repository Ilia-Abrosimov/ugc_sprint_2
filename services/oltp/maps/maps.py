"""
Модели данных.
"""

from pydantic import BaseModel, Field


class UserHistory(BaseModel):
    id: str = Field(title='uuid')
    user_id: str = Field(title='User id')
    film_id: str = Field(title='Film id')
    viewed_frame: int = Field(title='Film viewed frame')


class UserLikes(BaseModel):
    id: str = Field(title='uuid')
    film_id: str = Field(title='Film id')
    value: int = Field(title='Like or dislike')


class UserReview(BaseModel):
    id: str = Field(title='uuid')
    film_id: str = Field(title='Film id')
    text: str = Field(title='User film review')
    date: str = Field(title='Review date')


class UserReviewLikes(BaseModel):
    id: str = Field(title='uuid')
    review_id: str = Field(title='Review id')
    value: int = Field(title='Like or dislike')


class UserBookmarks(BaseModel):
    id: str = Field(title='uuid')
    film_id: str = Field(title='Film id')
