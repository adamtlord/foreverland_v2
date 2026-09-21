#!/usr/bin/env bash
# Stage and cut over prod from mysql:5.7 (./db) to MySQL 8 or MariaDB 10.11 (./db8).
# Never deletes ./db. Never mounts the live datadir into the new server.
#
#   ./scripts/cutover-mysql.sh stage      # dump 5.7, start db8, restore into ./db8
#   ./scripts/cutover-mysql.sh status
#   CUTOVER=1 ./scripts/cutover-mysql.sh cutover   # stop writes, final dump, swap ./db
#   ROLLBACK=1 ./scripts/cutover-mysql.sh rollback
#
# Optional: MYSQL_CUTOVER_IMAGE=mariadb:10.11 (default mysql:8.0)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

ENV_PROD="${REPO_ROOT}/.env.prod"
COMPOSE_PROD=(-f docker-compose.prod.yml)
COMPOSE_STAGE=(-f docker-compose.prod.yml -f docker-compose.db-cutover.yml)
LIVE_CONTAINER="${PROD_DB_CONTAINER:-foreverland_db}"
STAGE_CONTAINER="foreverland_db8"
LIVE_DATADIR="${REPO_ROOT}/db"
STAGE_DATADIR="${REPO_ROOT}/db8"
DUMP_DIR="${REPO_ROOT}/data/dumps"

usage() {
  echo "Usage: $0 stage|status|cutover|rollback" >&2
  echo "  MYSQL_CUTOVER_IMAGE=mysql:8.0 (default) or mariadb:10.11" >&2
  echo "  CUTOVER=1 $0 cutover" >&2
  echo "  ROLLBACK=1 $0 rollback" >&2
  exit 1
}

unquote() {
  local value="$1"
  value="${value%\"}"
  value="${value#\"}"
  value="${value%\'}"
  value="${value#\'}"
  printf '%s' "$value"
}

load_env_prod() {
  if [[ ! -f "$ENV_PROD" ]]; then
    echo "Missing .env.prod in repo root." >&2
    exit 1
  fi
  local image_override="${MYSQL_CUTOVER_IMAGE:-}"
  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" =~ ^[[:space:]]*# ]] || [[ -z "${line//[[:space:]]/}" ]]; then
      continue
    fi
    if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
      export "${BASH_REMATCH[1]}=$(unquote "${BASH_REMATCH[2]}")"
    fi
  done < "$ENV_PROD"
  for var in MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD MYSQL_ROOT_PASSWORD; do
    if [[ -z "${!var:-}" ]]; then
      echo "Missing $var in .env.prod" >&2
      exit 1
    fi
  done
  if [[ -n "$image_override" ]]; then
    export MYSQL_CUTOVER_IMAGE="$image_override"
  else
    export MYSQL_CUTOVER_IMAGE="${MYSQL_CUTOVER_IMAGE:-mysql:8.0}"
  fi
}

compose() {
  docker compose "${COMPOSE_PROD[@]}" "$@"
}

compose_stage() {
  docker compose "${COMPOSE_STAGE[@]}" "$@"
}

require_live_db() {
  if ! docker ps --format '{{.Names}}' | grep -q "^${LIVE_CONTAINER}$"; then
    echo "${LIVE_CONTAINER} is not running. Start prod db first." >&2
    exit 1
  fi
}

dump_live() {
  local dest="$1"
  mkdir -p "$(dirname "$dest")"
  echo "Dumping ${MYSQL_DATABASE} from ${LIVE_CONTAINER} to ${dest} ..."
  docker exec "$LIVE_CONTAINER" mysqldump \
    -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" \
    --single-transaction --no-tablespaces --routines --triggers \
    "$MYSQL_DATABASE" | gzip > "$dest"
  echo "Dump size: $(wc -c < "$dest" | tr -d ' ') bytes"
}

wait_for_mysql() {
  local container="$1"
  local tries=60
  local i
  for i in $(seq 1 "$tries"); do
    if docker exec "$container" mysqladmin ping -h127.0.0.1 -uroot -p"$MYSQL_ROOT_PASSWORD" --silent >/dev/null 2>&1; then
      return 0
    fi
    sleep 2
  done
  echo "${container} did not become ready in $((tries * 2))s." >&2
  docker logs "$container" --tail 50 >&2 || true
  exit 1
}

restore_to_stage() {
  local dump="$1"
  echo "Restoring ${dump} into ${STAGE_CONTAINER} as root ..."
  if [[ "$dump" == *.gz ]]; then
    gunzip -c "$dump" | docker exec -i "$STAGE_CONTAINER" \
      mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"
  else
    docker exec -i "$STAGE_CONTAINER" \
      mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" < "$dump"
  fi
}

print_version() {
  local container="$1"
  docker exec "$container" mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -Nse "SELECT VERSION();" 2>/dev/null \
    || docker exec "$container" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -Nse "SELECT VERSION();"
}

cmd_stage() {
  require_live_db
  if [[ -e "$STAGE_DATADIR" ]] && [[ -n "$(ls -A "$STAGE_DATADIR" 2>/dev/null || true)" ]]; then
    if [[ "${FORCE:-}" != "1" ]]; then
      echo "${STAGE_DATADIR} already has files. Refusing to reuse it." >&2
      echo "Move it aside, or rerun with FORCE=1 to destroy ./db8 only (never ./db)." >&2
      exit 1
    fi
    echo "FORCE=1: removing staging container and ${STAGE_DATADIR} (not ./db)"
    compose_stage stop db8 >/dev/null 2>&1 || true
    compose_stage rm -f db8 >/dev/null 2>&1 || true
    rm -rf "$STAGE_DATADIR"
  fi
  mkdir -p "$STAGE_DATADIR"

  local stamp
  stamp="$(date +%Y-%m-%d-%H%M%S)"
  local dump="${DUMP_DIR}/foreverland-cutover-stage-${stamp}.sql.gz"
  dump_live "$dump"

  echo "Starting ${STAGE_CONTAINER} (${MYSQL_CUTOVER_IMAGE}) on ${STAGE_DATADIR} ..."
  compose_stage up -d db8
  wait_for_mysql "$STAGE_CONTAINER"
  restore_to_stage "$dump"

  echo
  echo "Staged ${MYSQL_CUTOVER_IMAGE}: $(print_version "$STAGE_CONTAINER")"
  echo "Live mysql:5.7 still serving from ./db: $(print_version "$LIVE_CONTAINER")"
  echo "Dump kept at ${dump}"
  echo "Next: exercise finance on a spare web against MYSQL_HOST=${STAGE_CONTAINER}, then CUTOVER=1 $0 cutover"
}

cmd_status() {
  echo "Live datadir:  ${LIVE_DATADIR}"
  echo "Stage datadir: ${STAGE_DATADIR}"
  echo "Cutover image: ${MYSQL_CUTOVER_IMAGE:-mysql:8.0}"
  echo "PROD_DB_IMAGE: ${PROD_DB_IMAGE:-<unset, compose default mysql:5.7>}"
  if docker ps -a --format '{{.Names}} {{.Status}}' | grep -q "^${LIVE_CONTAINER} "; then
    echo -n "Live ${LIVE_CONTAINER}: "
    docker ps -a --format '{{.Names}} {{.Status}}' | grep "^${LIVE_CONTAINER} "
    if docker ps --format '{{.Names}}' | grep -q "^${LIVE_CONTAINER}$"; then
      echo "  version $(print_version "$LIVE_CONTAINER")"
    fi
  else
    echo "Live ${LIVE_CONTAINER}: not created"
  fi
  if docker ps -a --format '{{.Names}} {{.Status}}' | grep -q "^${STAGE_CONTAINER} "; then
    echo -n "Stage ${STAGE_CONTAINER}: "
    docker ps -a --format '{{.Names}} {{.Status}}' | grep "^${STAGE_CONTAINER} "
    if docker ps --format '{{.Names}}' | grep -q "^${STAGE_CONTAINER}$"; then
      echo "  version $(print_version "$STAGE_CONTAINER")"
    fi
  else
    echo "Stage ${STAGE_CONTAINER}: not created"
  fi
  ls -ld "$LIVE_DATADIR" "$STAGE_DATADIR" 2>/dev/null || true
  ls -d "${REPO_ROOT}"/db57-backup-* 2>/dev/null || true
}

set_prod_db_image() {
  local image="$1"
  if grep -q '^PROD_DB_IMAGE=' "$ENV_PROD"; then
    local tmp
    tmp="$(mktemp)"
    sed "s|^PROD_DB_IMAGE=.*|PROD_DB_IMAGE=${image}|" "$ENV_PROD" > "$tmp"
    mv "$tmp" "$ENV_PROD"
  else
    printf '\nPROD_DB_IMAGE=%s\n' "$image" >> "$ENV_PROD"
  fi
  export PROD_DB_IMAGE="$image"
}

cmd_cutover() {
  if [[ "${CUTOVER:-}" != "1" ]]; then
    echo "Refusing cutover without CUTOVER=1 (this stops web and swaps ./db)." >&2
    exit 1
  fi
  require_live_db
  if [[ ! -d "$STAGE_DATADIR" ]] || [[ -z "$(ls -A "$STAGE_DATADIR" 2>/dev/null || true)" ]]; then
    echo "No staged ./db8. Run $0 stage first." >&2
    exit 1
  fi
  if ! docker ps --format '{{.Names}}' | grep -q "^${STAGE_CONTAINER}$"; then
    echo "${STAGE_CONTAINER} is not running. Run $0 stage first." >&2
    exit 1
  fi

  echo "Stopping web so nothing writes to 5.7 ..."
  docker stop foreverland >/dev/null

  local stamp
  stamp="$(date +%Y-%m-%d-%H%M%S)"
  local dump="${DUMP_DIR}/foreverland-cutover-final-${stamp}.sql.gz"
  dump_live "$dump"
  restore_to_stage "$dump"

  echo "Stopping 5.7 and staging servers ..."
  docker stop "$LIVE_CONTAINER" "$STAGE_CONTAINER" >/dev/null
  docker rm "$STAGE_CONTAINER" >/dev/null

  local backup="${REPO_ROOT}/db57-backup-${stamp}"
  echo "Renaming ./db -> ${backup}"
  echo "Renaming ./db8 -> ./db"
  mv "$LIVE_DATADIR" "$backup"
  mv "$STAGE_DATADIR" "$LIVE_DATADIR"

  set_prod_db_image "$MYSQL_CUTOVER_IMAGE"
  echo "PROD_DB_IMAGE=${MYSQL_CUTOVER_IMAGE} written to .env.prod"

  echo "Starting cut-over db + web ..."
  compose up -d db
  wait_for_mysql "$LIVE_CONTAINER"
  echo "Now running $(print_version "$LIVE_CONTAINER")"
  compose up -d web

  echo
  echo "Cutover complete. 5.7 files are in ${backup} — keep them for a week."
  echo "foreverland.mysql57 still works on 8 / 10.11. After a soak, switch ENGINE to django.db.backends.mysql and delete web/foreverland/mysql57/."
}

cmd_rollback() {
  if [[ "${ROLLBACK:-}" != "1" ]]; then
    echo "Refusing rollback without ROLLBACK=1." >&2
    exit 1
  fi
  local latest
  latest="$(ls -1d "${REPO_ROOT}"/db57-backup-* 2>/dev/null | tail -n 1 || true)"
  if [[ -z "$latest" ]]; then
    echo "No ${REPO_ROOT}/db57-backup-* directory. Nothing to roll back to." >&2
    exit 1
  fi
  echo "Rolling back to ${latest}"
  docker stop foreverland "$LIVE_CONTAINER" >/dev/null 2>&1 || true
  if [[ -d "$LIVE_DATADIR" ]]; then
    local aside="${REPO_ROOT}/db8-failed-$(date +%Y-%m-%d-%H%M%S)"
    echo "Moving current ./db aside to ${aside}"
    mv "$LIVE_DATADIR" "$aside"
  fi
  mv "$latest" "$LIVE_DATADIR"
  set_prod_db_image "mysql:5.7"
  compose up -d db
  wait_for_mysql "$LIVE_CONTAINER"
  echo "Restored $(print_version "$LIVE_CONTAINER")"
  compose up -d web
  echo "Rollback complete. Web is on mysql:5.7 + ./db again."
}

if [[ $# -ne 1 ]]; then
  usage
fi

load_env_prod
case "$1" in
  stage) cmd_stage ;;
  status) cmd_status ;;
  cutover) cmd_cutover ;;
  rollback) cmd_rollback ;;
  *) usage ;;
esac
