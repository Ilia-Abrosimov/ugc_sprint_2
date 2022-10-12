FROM python:3.10-slim

WORKDIR /opt/tests

COPY ./tests/click_house/requirements.txt requirements.txt

RUN  apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY tests/click_house/test_click_house.py .
COPY tests/base_test.py ./tests/
COPY storages ./storages/
COPY src ./src/
COPY utils ./utils/

CMD [ "python3", "test_click_house.py" ]
