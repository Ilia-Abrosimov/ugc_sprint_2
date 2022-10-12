import pytest
from api.v1.films import film_progress_bp
from core.config import settings
from extensions import jwt
from flask import Flask


def create_app():
    test_app = Flask(__name__)
    test_app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key
    jwt.init_app(test_app)
    test_app.register_blueprint(film_progress_bp)
    return test_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()
