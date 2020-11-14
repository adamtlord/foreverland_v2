FROM python:3.6

WORKDIR /home/ubuntu/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir mediafiles
COPY ./mediafiles ./mediafiles

COPY . .