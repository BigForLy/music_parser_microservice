FROM python:3.10.5

WORKDIR /usr/src/micro/music_parser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/micro/music_parser/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/micro/music_parser/
