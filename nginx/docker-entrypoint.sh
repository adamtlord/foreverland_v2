#!/usr/bin/env sh
set -e
if [ -z "$@" ]; then
  rm -rf /etc/nginx/conf.d/*
  ln -s /etc/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
  exec nginx -g "daemon off;"
else
  exec $@
fi