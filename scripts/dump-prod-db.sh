#!/usr/bin/env bash
# Dump the production database (run where prod stack is running, e.g. prod server).
# Requires: .env.prod in project root with MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD.
# Usage: from repo root, ./scripts/dump-prod-db.sh [output_file]
#   If output_file is omitted, writes to data/dumps/foreverland-dump-YYYY-MM-DD-HHMMSS.sql.gz

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

ENV_PROD="${REPO_ROOT}/.env.prod"
if [[ ! -f "$ENV_PROD" ]]; then
  echo "Missing .env.prod in repo root. Create it with MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD (and MYSQL_ROOT_PASSWORD if needed)." >&2
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
done < "$ENV_PROD"

for var in MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD; do
  if [[ -z "${!var:-}" ]]; then
    echo "Missing $var in .env.prod" >&2
    exit 1
  fi
done

CONTAINER="${PROD_DB_CONTAINER:-foreverland_db}"
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "Container ${CONTAINER} is not running. Start prod stack first (e.g. docker compose -f docker-compose.prod.yml up -d db)." >&2
  exit 1
fi

TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
DEFAULT_OUTPUT="data/dumps/foreverland-dump-${TIMESTAMP}.sql.gz"
OUTPUT_FILE="${1:-$DEFAULT_OUTPUT}"

mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "Dumping ${MYSQL_DATABASE} from container ${CONTAINER} to ${OUTPUT_FILE} ..."
docker exec "$CONTAINER" mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --single-transaction --no-tablespaces --routines --triggers "$MYSQL_DATABASE" | gzip > "$OUTPUT_FILE"
echo "Done. $(wc -c < "$OUTPUT_FILE" | tr -d ' ') bytes written."
