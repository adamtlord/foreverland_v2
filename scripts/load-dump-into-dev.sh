#!/usr/bin/env bash
# Load a SQL dump into the local dev database (run with dev stack up).
# Requires: .env in repo root with MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD.
# Usage: from repo root, ./scripts/load-dump-into-dev.sh <dump.sql.gz>
#   Or: ./scripts/load-dump-into-dev.sh <dump.sql>   (uncompressed)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <dump.sql.gz or dump.sql>" >&2
  exit 1
fi
DUMP_FILE="$1"
if [[ ! -f "$DUMP_FILE" ]]; then
  echo "File not found: $DUMP_FILE" >&2
  exit 1
fi

ENV_FILE="${REPO_ROOT}/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing .env in repo root." >&2
  exit 1
fi

# Load only VAR=value lines (avoids executing malformed or comment-like lines)
while IFS= read -r line || [[ -n "$line" ]]; do
  if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "${line//[[:space:]]/}" ]]; then
    continue
  fi
  if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
    export "${BASH_REMATCH[1]}=${BASH_REMATCH[2]}"
  fi
done < "$ENV_FILE"

for var in MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD; do
  if [[ -z "${!var:-}" ]]; then
    echo "Missing $var in .env" >&2
    exit 1
  fi
done

CONTAINER="${DEV_DB_CONTAINER:-foreverland_db}"
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "Container ${CONTAINER} is not running. Start dev stack first (e.g. docker compose up -d db)." >&2
  exit 1
fi

echo "Dropping and recreating database ${MYSQL_DATABASE} in ${CONTAINER} ..."
docker exec "$CONTAINER" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "
  DROP DATABASE IF EXISTS \`${MYSQL_DATABASE}\`;
  CREATE DATABASE \`${MYSQL_DATABASE}\` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"

echo "Loading dump into ${MYSQL_DATABASE} ..."
if [[ "$DUMP_FILE" == *.gz ]]; then
  gunzip -c "$DUMP_FILE" | docker exec -i "$CONTAINER" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"
else
  docker exec -i "$CONTAINER" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$DUMP_FILE"
fi
echo "Done."
