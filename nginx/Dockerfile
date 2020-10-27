FROM nginx:1.19.0-alpine

COPY ./ops/nginx.conf /etc/nginx/
COPY ./ops/docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

