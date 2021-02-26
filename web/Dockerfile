FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tmp
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y --no-install-recommends \
    nodejs

WORKDIR /home/ubuntu/app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN npm install -g --loglevel=error @vue/cli

COPY . .