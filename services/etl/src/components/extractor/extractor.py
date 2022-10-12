"""
Загрузчик данных из хранилища событий.

"""

from typing import Generator

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from src.components.extractor.base import BaseExtractor
from src.core.settings import etl_settings, kafka_settings


class KafkaExtractor(BaseExtractor):

    __slots__ = ('consumer', 'admin_client', 'producer', 'run')

    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=kafka_settings.bootstrap_servers,
            auto_offset_reset='latest',
            group_id=kafka_settings.group,
            enable_auto_commit=False,
        )
        self.admin_client = KafkaAdminClient(bootstrap_servers=kafka_settings.bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=kafka_settings.bootstrap_servers)
        self.run = True

    def consume(self) -> Generator:
        self.consumer.subscribe(kafka_settings.topics)
        while self.run:
            records = self.consumer.poll(
                max_records=etl_settings.batch_size,
                timeout_ms=etl_settings.kafka_consumer_timeout,
            )
            yield records

        self.consumer.close()

    def stop_consuming(self) -> None:
        self.run = False

    def commit(self) -> None:
        self.consumer.commit()
