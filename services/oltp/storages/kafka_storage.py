from core.config import kafka_settings
from kafka import KafkaProducer


class KafkaStorage:

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=kafka_settings.bootstrap_servers)

    def send(self, body, topic: str):
        value = str.encode(body.json())
        if 'review_id' not in body.dict().keys():
            key = str.encode(f'{topic}+{body.user_id}+{body.film_id}')
        else:
            key = str.encode(f'{topic}+{body.user_id}+{body.review_id}')
        self.producer.send(topic=topic, value=value, key=key)

        return
