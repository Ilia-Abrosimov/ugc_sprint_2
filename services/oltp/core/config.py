from pydantic import BaseSettings


class Settings(BaseSettings):
    app_host: str = 'localhost'
    debug: bool = False
    jwt_secret_key: str = 'top_secret'
    test_api_url: str = "http://kafka-test:9093/api/v1/"
    api_version: str
    swagger_path: str
    sentry_sdk: str = 'SDK'


class KafkaSettings(BaseSettings):
    bootstrap_servers: list[str]
    topics: list[str]
    group: str
    views_topic: str

    class Config:
        env_prefix = 'KAFKA_'


class MongoSettings(BaseSettings):
    host: str
    port: str

    class Config:
        env_prefix = 'MONGO_'


settings = Settings()
kafka_settings = KafkaSettings()
mongo_settings = MongoSettings()
