from core import settings


class EventStoreTest:
    def __init__(self, client, stream: str = 'test-stream'):
        self.client = client
        self.stream = stream

    async def writer(self):
        async with self.client.connect() as conn:
            for i in range(settings.MSG_COUNT):
                await conn.streams.append(stream=self.stream, event_type='test_event', data=settings.MSG_DATA)
        return settings.MSG_COUNT

    async def reader(self):
        async with self.client.connect() as conn:
            msg_count = 0
            async for result in conn.streams.read(stream=self.stream, count=settings.MSG_COUNT):
                msg_count += 1
                if msg_count >= settings.MSG_COUNT:
                    break
        return msg_count

    async def clear_stream(self):
        async with self.client.connect() as conn:
            await conn.streams.delete(stream=self.stream)
