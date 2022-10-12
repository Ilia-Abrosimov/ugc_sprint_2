FROM python:3.10-slim

WORKDIR /opt/tests

COPY ./tests/click_house_shard/requirements.txt requirements.txt

RUN  apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY tests/click_house_shard/test.py .
COPY click_house ./click_house/
COPY src ./src/
COPY utils ./utils/

CMD [ "python3", "test.py" ]
