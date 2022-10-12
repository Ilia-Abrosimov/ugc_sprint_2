from app import spec
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from maps.maps import UserReviewLikes
from schemas.review_likes import (DeleteReviewLikeParams, DeleteReviewLikeResponse, GetUserLikesParams,
                                  GetUserLikesResponse, LikeReviewBody, LikeReviewParams, LikeReviewResponse,
                                  UpdateReviewLikeBody, UpdateReviewLikeParams, UpdateReviewLikeResponse)
from storages.mongo_storage import MongoStorage
from utils.injectors import hot_storage_injector
from utils.json_response import json_response
from utils.unpack import unpack_models

review_likes_bp = Blueprint('review_likes', __name__, url_prefix='/api/v1/review_likes')
TAG = 'Review likes'
DB_NAME = 'default'
TABLE = 'review_likes'


@review_likes_bp.route('/', methods=['POST'])
@spec.validate(
    query=LikeReviewParams,
    body=LikeReviewBody,
    resp=Response(HTTP_200=LikeReviewResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def create_like(
        query: LikeReviewParams,
        body: LikeReviewBody,
        storage: MongoStorage,
) -> LikeReviewResponse:
    """ Like/dislike review.
        ---
    """
    data = {'user_id': str(query.user_id), 'review_id': str(body.review_id), 'value': body.value}
    loop = storage.client.get_io_loop()

    result = loop.run_until_complete(storage.add(db_name=DB_NAME, table=TABLE, data=data, search='review_id'))

    return LikeReviewResponse(message=f'Оценка {result} к обзору {str(body.review_id)} добавлена.')


@review_likes_bp.route('/', methods=['GET'])
@spec.validate(
    query=GetUserLikesParams,
    resp=Response(HTTP_200=GetUserLikesResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def get_user_likes(query: GetUserLikesParams, storage: MongoStorage) -> GetUserLikesResponse:
    """ Get user reviews likes/dislikes.
        ---
    """
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.read_many(db_name=DB_NAME, table=TABLE, user_id=str(query.user_id)))

    return GetUserLikesResponse(reviews=[UserReviewLikes(**item, id=str(item['_id'])) for item in result])


@review_likes_bp.route('/', methods=['PUT'])
@spec.validate(
    query=UpdateReviewLikeParams,
    body=UpdateReviewLikeBody,
    resp=Response(HTTP_200=UpdateReviewLikeResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def update_review_like(
        query: UpdateReviewLikeParams,
        body: UpdateReviewLikeBody,
        storage: MongoStorage,
) -> UpdateReviewLikeResponse:
    """ Update review like.
        ---
    """
    data = {'user_id': str(query.user_id), 'review_id': str(body.review_id), 'value': body.value}
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.update(db_name=DB_NAME, table=TABLE, data=data, search='review_id'))

    return UpdateReviewLikeResponse(message=f'Оценка {result} к обзору {str(body.review_id)} обновлена.')


@review_likes_bp.route('/', methods=['DELETE'])
@spec.validate(
    query=DeleteReviewLikeParams,
    resp=Response(HTTP_200=DeleteReviewLikeResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def delete_review_like(query: DeleteReviewLikeParams, storage: MongoStorage) -> DeleteReviewLikeResponse:
    """ Delete review like/dislike.
        ---
    """
    loop = storage.client.get_io_loop()
    loop.run_until_complete(storage.delete(db_name=DB_NAME, table=TABLE, obj_id=str(query.like_id)))

    return DeleteReviewLikeResponse(message=f'Оценка {str(query.like_id)} удалена.')
