import logging

import logstash
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from core.config import settings
from extensions import jwt
from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec


spec = FlaskPydanticSpec('flask', title='UGC API', version=settings.api_version, path=settings.swagger_path)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


sentry_sdk.init(
    dsn=settings.sentry_sdk,
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)


def create_app():
    from api.v1.bookmarks import bookmarks_bp
    from api.v1.films import film_progress_bp
    from api.v1.likes import likes_bp
    from api.v1.review_likes import review_likes_bp
    from api.v1.reviews import reviews_bp

    app = Flask(__name__)
    app.register_blueprint(film_progress_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(likes_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(review_likes_bp)
    app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key
    app.logger = logging.getLogger(__name__)
    app.logger.setLevel(logging.INFO)
    logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)
    app.logger.addHandler(logstash_handler)
    app.logger.addFilter(RequestIdFilter())

    # @app.before_request
    # def before_request():
    #     request_id = request.headers.get('X-Request-Id')
    #     if not request_id:
    #         raise RuntimeError('request id is required')

    jwt.init_app(app)
    spec.register(app)

    return app
