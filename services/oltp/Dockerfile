FROM python:3.9

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip -r requirements.txt
RUN apt-get update && apt-get install -y netcat

COPY . /app
EXPOSE 5000