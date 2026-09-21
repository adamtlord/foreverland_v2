#!/usr/bin/env bash
# Production compose wrapper. Always uses docker-compose.prod.yml.
# Usage (from repo root, on the Ubuntu host):
#   ./scripts/deploy-prod.sh down
#   ./scripts/deploy-prod.sh up -d --build --force-recreate
#   ./scripts/deploy-prod.sh config
#   ./scripts/deploy-prod.sh ps
#
# Never pass --remove-orphans (would drop nginx/certbot TLS containers).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <docker compose args>" >&2
  echo "  $0 down" >&2
  echo "  $0 up -d --build --force-recreate" >&2
  echo "  $0 config" >&2
  exit 1
fi

for arg in "$@"; do
  if [[ "$arg" == "--remove-orphans" ]]; then
    echo "Refusing --remove-orphans: that can delete prod nginx/certbot (TLS)." >&2
    exit 1
  fi
done

ENV_PROD="${REPO_ROOT}/.env.prod"
if [[ ! -f "$ENV_PROD" ]]; then
  echo "Missing .env.prod in repo root." >&2
  exit 1
fi

has_root_password=0
PROD_DB_IMAGE=""
while IFS= read -r line || [[ -n "$line" ]]; do
  if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "${line//[[:space:]]/}" ]]; then
    continue
  fi
  if [[ "$line" =~ ^(MYSQL_ROOT_PASSWORD|MARIADB_ROOT_PASSWORD)=(.+)$ ]]; then
    value="${BASH_REMATCH[2]}"
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"
    if [[ -n "$value" ]]; then
      has_root_password=1
    fi
  fi
  if [[ "$line" =~ ^PROD_DB_IMAGE=(.+)$ ]]; then
    value="${BASH_REMATCH[1]}"
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"
    PROD_DB_IMAGE="$value"
    export PROD_DB_IMAGE
  fi
done < "$ENV_PROD"

if [[ "$has_root_password" -ne 1 ]]; then
  echo ".env.prod must set a non-empty MYSQL_ROOT_PASSWORD (or MARIADB_ROOT_PASSWORD)." >&2
  echo "MYSQL_PASSWORD is the Django/app user only and is not enough for MySQL/MariaDB init." >&2
  exit 1
fi

if docker inspect foreverland_db >/dev/null 2>&1; then
  image="$(docker inspect foreverland_db --format '{{.Config.Image}}')"
  if [[ "$image" == mariadb* && -z "$PROD_DB_IMAGE" ]]; then
    echo "Warning: foreverland_db is currently ${image} (dev image), not mysql:5.7." >&2
    echo "Remove those containers before prod up. Do not delete ./db:" >&2
    echo "  docker stop foreverland foreverland_db && docker rm foreverland foreverland_db" >&2
    for arg in "$@"; do
      if [[ "$arg" == "up" ]]; then
        exit 1
      fi
    done
  fi
fi

exec docker compose -f docker-compose.prod.yml "$@"
