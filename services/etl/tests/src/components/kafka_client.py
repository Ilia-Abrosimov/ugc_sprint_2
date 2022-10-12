"""
Клиент Kafka.

Создание топиков и сообщений для тестов.

"""

from etl.src.core.settings import kafka_settings
from kafka import KafkaAdminClient, KafkaProducer, errors
from kafka.admin import NewTopic


class KafkaClient:

    def __init__(self):
        self.admin_client = KafkaAdminClient(bootstrap_servers=kafka_settings.bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=kafka_settings.bootstrap_servers)

    def create_topics(self, topics: list):
        topics = [
            NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
            for topic_name in topics
        ]
        try:
            self.admin_client.create_topics(topics)
        except errors.TopicAlreadyExistsError:
            pass

    def delete_topics(self, topics: list):
        self.admin_client.delete_topics(topics)

    def produce(self, topic: str, messages: list):
        for message in messages:
            self.producer.send(
                topic=topic,
                value=message,
            )
