FROM nginx:1.19.0-alpine
RUN chmod 777 /home/ubuntu/app/nginx/docker-entrypoint.sh \
    && ln -s /home/ubuntu/app/nginx/docker-entrypoint.sh /
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d