from uuid import UUID

from maps.maps import UserBookmarks
from pydantic import BaseModel, Field


class CreateBookmarkParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, который создает закладку')


class CreateBookmarkBody(BaseModel):
    film_id: UUID = Field(title='id фильма, добавляемого в закладки')


class CreateBookmarkResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')


class GetBookmarksParams(BaseModel):
    user_id: UUID = Field(title='id пользователя, запрашивающего список закладок')


class GetBookmarksResponse(BaseModel):
    bookmarks: list[UserBookmarks] = Field(title='Список закладок пользователя')


class DeleteBookmarkParams(BaseModel):
    bookmark_id: str = Field(title='id удаляемой закладки')


class DeleteBookmarkResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')
