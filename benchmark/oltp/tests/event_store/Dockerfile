FROM python:3.9

WORKDIR /opt/tests

COPY ./tests/event_store/requirements.txt requirements.txt

RUN pip3 install --upgrade pip -r requirements.txt

COPY tests/event_store/eventstore_test.py .
COPY core ./core/
COPY utils ./utils/
COPY event_store ./event_store/
COPY tests/logs ./logs/

CMD [ "python3", "eventstore_test.py" ]
