FROM nginx:1.19.0-alpine

COPY ./nginx.conf /etc/nginx/
COPY ./docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

