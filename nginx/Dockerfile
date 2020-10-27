FROM nginx:1.19.0-alpine

COPY /nginx/nginx.conf /etc/nginx/
COPY /nginx/docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

