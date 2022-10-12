from core import settings
from kafka import KafkaConsumer, KafkaProducer


class KafkaTest:
    def __init__(self, bootstrap_servers: list, topic: str = 'test-topic'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

    def producer(self):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        for i in range(settings.MSG_COUNT):
            producer.send(self.topic, settings.MSG_DATA)
        producer.flush()

    def consumer(self):
        consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers, auto_offset_reset='earliest', group_id=None)
        msg_count = 0
        consumer.subscribe([self.topic])
        for msg in consumer:
            msg_count += 1
            if msg_count >= settings.MSG_COUNT:
                break
        consumer.close()
        return msg_count
