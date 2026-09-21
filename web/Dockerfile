FROM python:3.12-slim-bookworm

WORKDIR /home/ubuntu/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" appuser

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x /home/ubuntu/app/entrypoint.sh \
    && mkdir -p /home/ubuntu/app/staticfiles /home/ubuntu/app/mediafiles \
    && chown -R appuser:appuser /home/ubuntu/app

# collectstatic/migrate run as root so named volumes are writable;
# entrypoint then drops to appuser for gunicorn.
CMD ["/home/ubuntu/app/entrypoint.sh"]
