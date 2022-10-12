FROM python:3.10-slim

WORKDIR /opt/etl

COPY . .

RUN  apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

CMD [ "python3", "manager.py" ]
