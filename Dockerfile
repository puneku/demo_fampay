FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /fampay_container

ADD . /fampay_container

COPY ./requirements.txt /fampay_container/requirements.txt

RUN pip install -r requirements.txt

COPY . /fampay_container

