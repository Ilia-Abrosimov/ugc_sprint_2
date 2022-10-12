from threading import Thread

from kafka_db.client import KafkaTest
from kafka_db.local_tests.utils.utils import KafkaContainer
from utils.timing import Timing

pending = True


def read(client):
    global pending
    while pending:
        client.consumer()


def read_and_write(client):
    global pending
    writing = Thread(target=client.producer)
    reading = Thread(target=read, args=(client,))
    writing.start()
    reading.start()
    writing.join()
    pending = False
    reading.join()


if __name__ == '__main__':
    with KafkaContainer() as kafka_container:
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_test = KafkaTest(bootstrap_server)

        with Timing(message='Kafka producer') as producer_timing:
            kafka_test.producer()

        with Timing(message='Kafka consumer') as consumer_timing:
            consumer_timing.n_messages = kafka_test.consumer()

        with Timing(message='Kafka read and write') as read_and_write_timing:
            read_and_write(kafka_test)
