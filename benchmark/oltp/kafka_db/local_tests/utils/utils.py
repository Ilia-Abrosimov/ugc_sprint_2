import sys

from testcontainers.kafka import KafkaContainer


class WinKafkaContainer(KafkaContainer):
    def get_container_host_ip(self):
        return super().get_container_host_ip().replace('localnpipe', 'localhost')


if sys.platform == 'win32':
    KafkaContainer = WinKafkaContainer
