import asyncio

from core import es_settings
from esdb import ESClient
from event_store.client import EventStoreTest
from utils.timing import Timing


async def read_and_write(client):
    task_1 = asyncio.create_task(client.writer())
    done, pending = await asyncio.wait([task_1], timeout=0)
    while task_1 not in done:
        await client.reader()
        done, pending = await asyncio.wait([task_1], timeout=0)

    await task_1


if __name__ == '__main__':
    esdb_test = EventStoreTest(client=ESClient(f'{es_settings.ESDB_HOST}:{es_settings.ESDB_PORT}', insecure=True))

    with Timing(message='EventStore writer') as writer_timing:
        asyncio.run(esdb_test.writer())

    with Timing(message='EventStore reader') as reader_timing:
        asyncio.run(esdb_test.reader())

    with Timing(message='EventStore read and write') as read_and_write_timing:
        asyncio.run(read_and_write(esdb_test))

    asyncio.run(esdb_test.clear_stream())
