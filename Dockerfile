FROM python:3.9-alpine3.16

ENV PROJECT_DIR /usr/src/app
WORKDIR ${PROJECT_DIR}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev \
    && apk add libxml2-dev libxslt-dev python3-dev gcc build-base

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .