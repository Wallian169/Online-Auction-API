FROM python:3.12-slim

LABEL maintainer="wallain169@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /files/media

RUN adduser --disabled-password --no-create-home my_user
RUN chown -R my_user /files/media
RUN chmod -R 755 /files/media

USER my_user
