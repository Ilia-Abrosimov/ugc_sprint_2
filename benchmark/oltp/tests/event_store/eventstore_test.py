import asyncio

from core import es_settings
from esdb import ESClient
from event_store.client import EventStoreTest
from utils.timing import Timing

if __name__ == '__main__':
    esdb_test = EventStoreTest(client=ESClient(f'{es_settings.ESDB_HOST}:{es_settings.ESDB_PORT}', insecure=True))

    with Timing(message='EventStore writer') as writer_timing:
        asyncio.run(esdb_test.writer())

    with Timing(message='EventStore reader') as reader_timing:
        asyncio.run(esdb_test.reader())

    asyncio.run(esdb_test.clear_stream())
