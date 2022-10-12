from pydantic import BaseSettings


class Settings(BaseSettings):
    MSG_COUNT: int = 1000
    MSG_SIZE: int = 10
    MSG_DATA: bytes = ('testmessage' * 20).encode()[:MSG_SIZE]
    LOG_FILE: str = './logs/tests.log'


class EventStoreSettings(BaseSettings):
    ESDB_HOST: str = 'localhost'
    ESDB_PORT: int = 2113


class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: list[str] = ['kafka1:19092', 'localhost:9021']


settings = Settings()
es_settings = EventStoreSettings()
kafka_settings = KafkaSettings()
