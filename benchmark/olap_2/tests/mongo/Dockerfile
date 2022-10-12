FROM python:3.10-slim

WORKDIR /opt/tests

COPY ./tests/mongo/requirements.txt requirements.txt

RUN  apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY tests/mongo/test_mongo.py .
COPY tests/base_test.py ./tests/
COPY storages ./storages/
COPY src ./src/
COPY utils ./utils/

CMD [ "python3", "test_mongo.py" ]
