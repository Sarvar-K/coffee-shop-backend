FROM python:3.11-slim

WORKDIR /app

EXPOSE 8000

VOLUME /app/keys

ADD requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

ADD src ./src

WORKDIR /app/src
CMD gunicorn