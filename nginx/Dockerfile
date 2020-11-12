FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
RUN chmod +x docker-entrypoint.sh
COPY nginx.conf /etc/nginx/conf.d