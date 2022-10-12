FROM python:3.9

WORKDIR /opt/tests

COPY ./tests/kafka_db/requirements.txt requirements.txt

RUN pip3 install --upgrade pip -r requirements.txt

COPY tests/kafka_db/kafka_test.py .
COPY core ./core/
COPY utils ./utils/
COPY kafka_db ./kafka_db/
COPY tests/logs ./logs/

CMD [ "python3", "kafka_test.py" ]
