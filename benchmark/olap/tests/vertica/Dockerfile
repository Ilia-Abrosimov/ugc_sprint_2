FROM python:3.10-slim

WORKDIR /opt/tests

COPY ./tests/vertica/requirements.txt requirements.txt

RUN  apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY tests/vertica/test.py .
COPY src ./src/
COPY utils ./utils/
COPY vertica ./vertica/

CMD [ "python3", "test.py" ]
