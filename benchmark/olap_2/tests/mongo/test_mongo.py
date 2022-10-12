from threading import Thread

from src.settings import settings
from storages.mongo.client import MongoClient
from tests.base_test import BaseStorageTest
from utils.logger import mongo_logger as logger
from utils.timer import Timer


class TestMongo(BaseStorageTest):
    """ """


if __name__ == '__main__':
    local = False
    test_client = TestMongo(
        client=MongoClient(local=local),
        batch_size=settings.mongo_batch_size,
    )

    with Timer(logger=logger, message=f'write data DV={settings.data_volume} BS={settings.mongo_batch_size}'):
        test_client.test_write()

    with Timer(logger=logger, message=f'read data DV={settings.data_volume} RN={settings.requests_num * 3}'):
        for _ in range(settings.requests_num):
            test_client.test_read()

    with Timer(
            logger=logger,
            message=f'write/read data DV={settings.data_volume} BS={settings.mongo_batch_size}',
    ):
        write = Thread(target=test_client.test_write)
        read = Thread(target=test_client.read_in_parallel)
        write.start()
        read.start()
        write.join()
        test_client.pending = False
        read.join()
