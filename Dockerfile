FROM python:3.12-alpine3.19

COPY requirements.txt /temp/requirements.txt
COPY quiz_service /service

WORKDIR /service

EXPOSE 8000
RUN apk add  postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password quiz-user

USER quiz-user