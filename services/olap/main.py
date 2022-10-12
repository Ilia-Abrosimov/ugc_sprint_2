import os

from clickhouse_driver import Client
from core.settings import ch_settings, mongo_settings, settings
from loguru import logger
from pymongo import MongoClient
from src.ch_handler import ClickHouseHandler
from src.mongo_handler import MongoHandler

log_file = settings.LOG_FILE
logger.add(log_file, rotation=settings.LOG_FILE_ROTATION)

if __name__ == '__main__':
    ch_client = Client(host=ch_settings.host, port=ch_settings.port, alt_hosts=ch_settings.hosts_str)
    ch_handler = ClickHouseHandler(ch_client)

    logger.info(f'{os.path.abspath(log_file)}')
    logger.info(ch_handler.get_top_by_views(settings.GET_TOP_AMOUNT))
    logger.info(ch_handler.get_top_by_rating(settings.GET_TOP_AMOUNT))

    mongo_client: MongoClient = MongoClient(f'mongodb://{mongo_settings.host}:{mongo_settings.port}/')
    mongo_handler = MongoHandler(mongo_client, mongo_settings.db)
    # TODO: расширение функционала (реализована выборка по пользователю)
