FROM python:3.9

WORKDIR /opt/olap

COPY ./requirements.txt requirements.txt

RUN pip3 install --upgrade pip -r requirements.txt --no-cache-dir

COPY . .
