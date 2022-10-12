from app import spec
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from maps.maps import UserReview
from schemas.reviews import (CreateReviewBody, CreateReviewParams, CreateReviewResponse, DeleteReviewParams,
                             DeleteReviewResponse, GetUserReviewParams, GetUserReviewResponse, GetUserReviewsParams,
                             GetUserReviewsResponse, UpdateReviewBody, UpdateReviewParams, UpdateReviewResponse)
from storages.mongo_storage import MongoStorage
from utils.injectors import hot_storage_injector
from utils.json_response import json_response
from utils.unpack import unpack_models

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/v1/reviews')
TAG = 'Reviews'
DB_NAME = 'default'
TABLE = 'reviews'


@reviews_bp.route('/', methods=['POST'])
@spec.validate(
    query=CreateReviewParams,
    body=CreateReviewBody,
    resp=Response(HTTP_200=CreateReviewResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def create_review(query: CreateReviewParams, body: CreateReviewBody, storage: MongoStorage) -> CreateReviewResponse:
    """ Create review.
        ---
    """
    data = {
        'user_id': str(query.user_id),
        'date': str(body.date),
        'film_id': str(body.film_id),
        'text': body.text,
    }
    loop = storage.client.get_io_loop()

    result = loop.run_until_complete(storage.add(db_name=DB_NAME, table=TABLE, data=data))

    return CreateReviewResponse(message=f'Обзор {result}, созданный пользователем {str(query.user_id)}, добавлен.')


@reviews_bp.route('/', methods=['GET'])
@spec.validate(
    query=GetUserReviewsParams,
    resp=Response(HTTP_200=GetUserReviewsResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def get_reviews(query: GetUserReviewsParams, storage: MongoStorage) -> GetUserReviewsResponse:
    """ Get user reviews.
        ---
    """
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.read_many(db_name=DB_NAME, table=TABLE, user_id=str(query.user_id)))

    return GetUserReviewsResponse(reviews=[UserReview(**item, id=str(item['_id'])) for item in result])


@reviews_bp.route('/review/', methods=['GET'])
@spec.validate(
    query=GetUserReviewParams,
    resp=Response(HTTP_200=GetUserReviewResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def get_review(query: GetUserReviewParams, storage: MongoStorage) -> GetUserReviewResponse:
    """ Get review.
        ---
    """
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.read_one(db_name=DB_NAME, table=TABLE, obj_id=str(query.review_id)))

    return GetUserReviewResponse(review=UserReview(**result, id=str(result['_id'])))


@reviews_bp.route('/', methods=['PUT'])
@spec.validate(
    query=UpdateReviewParams,
    body=UpdateReviewBody,
    resp=Response(HTTP_200=UpdateReviewResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def update_review(query: UpdateReviewParams, body: UpdateReviewBody, storage: MongoStorage) -> UpdateReviewResponse:
    """ Update review.
        ---
    """
    data = {
        'user_id': str(query.user_id),
        'date': str(body.date),
        'film_id': str(body.film_id),
        'text': body.text,
    }
    loop = storage.client.get_io_loop()
    result = loop.run_until_complete(storage.update(db_name=DB_NAME, table=TABLE, data=data))

    return UpdateReviewResponse(message=f'Обзор {result}, созданный пользователем {str(query.user_id)}, обновлен.')


@reviews_bp.route('/', methods=['DELETE'])
@spec.validate(
    query=DeleteReviewParams,
    resp=Response(HTTP_200=DeleteReviewResponse),
    tags=[TAG],
)
@unpack_models
@json_response
@jwt_required()
@hot_storage_injector
def remove_review(query: DeleteReviewParams, storage: MongoStorage) -> DeleteReviewResponse:
    """ Remove review.
        ---
    """
    loop = storage.client.get_io_loop()
    loop.run_until_complete(storage.delete(db_name=DB_NAME, table=TABLE, obj_id=str(query.review_id)))

    return DeleteReviewResponse(message=f'Обзор {str(query.review_id)} удален.')
