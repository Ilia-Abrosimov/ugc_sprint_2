import math
import time
import unittest

from etl.src.components.extractor.extractor import KafkaExtractor
from etl.src.core.settings import etl_settings, kafka_settings
from tests.src.components.kafka_client import KafkaClient
from tests.src.models.models import UserHistory


class TestExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = KafkaExtractor()
        self.text_client = KafkaClient()

        self.messages = {}
        self.amount = 3

        self.text_client.create_topics(topics=kafka_settings.topics)
        for topic in kafka_settings.topics:
            topic_messages = [str(UserHistory().dict()).encode() for _ in range(self.amount)]
            self.messages[topic] = topic_messages
            self.text_client.produce(topic=topic, messages=topic_messages)

    def tearDown(self):
        self.text_client.delete_topic(topics=kafka_settings.topics)

    def test_messages(self):
        records = self.extractor.consume()
        for _ in range(math.ceil(self.amount * len(kafka_settings.topics)/etl_settings.batch_size)):
            try:
                data_dict = next(records)
            except StopIteration:
                time.sleep(etl_settings.etl_manager_timeout)
            else:
                for key, value in data_dict.items():
                    for record in value:
                        assert record.value == self.messages[record.topic].pop(0)

        self.extractor.stop_consuming()


if __name__ == '__main__':
    unittest.main()
