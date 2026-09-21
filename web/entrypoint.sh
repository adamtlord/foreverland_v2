#!/bin/bash
set -euo pipefail

python3 manage.py collectstatic --noinput
python3 manage.py compress
python3 manage.py repair_migration_history
python3 manage.py migrate --noinput

exec runuser -u appuser -- gunicorn foreverland.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 30
