#!/usr/bin/env bash
# Stage and cut over prod from mysql:5.7 (./db) to MySQL 8 or MariaDB 10.11 (./db8).
# Never deletes ./db. Never mounts the live datadir into the new server.
#
#   ./scripts/cutover-mysql.sh stage
#   ./scripts/cutover-mysql.sh status
#   CUTOVER=1 ./scripts/cutover-mysql.sh cutover
#   ROLLBACK=1 ./scripts/cutover-mysql.sh rollback
#   ./scripts/cutover-mysql.sh import-dump [path.sql.gz]   # load a dump into live
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
# Django tables that must have rows after a real restore.
CANARY_TABLES=(shows_show members_member auth_user)

usage() {
  echo "Usage: $0 stage|status|cutover|rollback|import-dump [dump.sql.gz]" >&2
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
  if [[ "$MYSQL_CUTOVER_IMAGE" == *5.7* ]]; then
    echo "MYSQL_CUTOVER_IMAGE=${MYSQL_CUTOVER_IMAGE} is still 5.7. Set mysql:8.0 or mariadb:10.11." >&2
    exit 1
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

# .env.prod sets MYSQL_HOST=db. Inside db8 that points at live 5.7, so every
# client must pin 127.0.0.1 and clear MYSQL_HOST.
mysql_local() {
  local container="$1"
  shift
  docker exec -e MYSQL_HOST=127.0.0.1 -e MYSQL_UNIX_PORT= "$container" "$@"
}

mysql_root() {
  local container="$1"
  shift
  mysql_local "$container" mysql \
    -h127.0.0.1 \
    -uroot -p"$MYSQL_ROOT_PASSWORD" \
    --init-command="SET SESSION sql_mode=''" \
    "$@"
}

count_tables() {
  local container="$1"
  mysql_root "$container" -Nse \
    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='${MYSQL_DATABASE}' AND table_type='BASE TABLE';"
}

count_rows() {
  local container="$1"
  local table="$2"
  mysql_root "$container" -Nse \
    "SELECT COUNT(*) FROM \`${MYSQL_DATABASE}\`.\`${table}\`;" 2>/dev/null || echo 0
}

summarize_db() {
  local container="$1"
  local tables rows
  tables="$(count_tables "$container")"
  echo "${container}: ${tables} tables in ${MYSQL_DATABASE}"
  local table
  for table in "${CANARY_TABLES[@]}"; do
    rows="$(count_rows "$container" "$table")"
    echo "  ${table}: ${rows} rows"
  done
}

assert_has_data() {
  local container="$1"
  local label="$2"
  local tables rows
  tables="$(count_tables "$container" | tr -cd '0-9')"
  if [[ "${tables:-0}" -lt 10 ]]; then
    echo "${label}: ${container} has ${tables:-0} tables (need >= 10). Refusing." >&2
    summarize_db "$container" >&2
    return 1
  fi
  local ok=0
  local table
  for table in "${CANARY_TABLES[@]}"; do
    rows="$(count_rows "$container" "$table" | tr -cd '0-9')"
    if [[ "${rows:-0}" -gt 0 ]]; then
      ok=1
      break
    fi
  done
  if [[ "$ok" -ne 1 ]]; then
    echo "${label}: ${container} has schema but canary tables are empty. Refusing." >&2
    summarize_db "$container" >&2
    return 1
  fi
  summarize_db "$container"
}

dump_live() {
  local dest="$1"
  mkdir -p "$(dirname "$dest")"
  echo "Dumping ${MYSQL_DATABASE} from ${LIVE_CONTAINER} (as root) to ${dest} ..."
  mysql_local "$LIVE_CONTAINER" mysqldump \
    -h127.0.0.1 \
    -uroot -p"$MYSQL_ROOT_PASSWORD" \
    --single-transaction --no-tablespaces --routines --triggers --set-gtid-purged=OFF \
    "$MYSQL_DATABASE" | gzip > "$dest"
  local bytes
  bytes="$(wc -c < "$dest" | tr -d ' ')"
  echo "Dump size: ${bytes} bytes"
  if [[ "${bytes:-0}" -lt 10000 ]]; then
    echo "Dump is too small (${bytes} bytes). Not a real foreverland dump." >&2
    exit 1
  fi
}

wait_for_mysql() {
  local container="$1"
  local tries=60
  local i
  for i in $(seq 1 "$tries"); do
    if mysql_local "$container" mysqladmin ping -h127.0.0.1 -uroot -p"$MYSQL_ROOT_PASSWORD" --silent >/dev/null 2>&1; then
      return 0
    fi
    sleep 2
  done
  echo "${container} did not become ready in $((tries * 2))s." >&2
  docker logs "$container" --tail 50 >&2 || true
  exit 1
}

restore_dump() {
  local dump="$1"
  local container="$2"
  echo "Restoring ${dump} into ${container} as root (sql_mode empty) ..."
  if [[ "$dump" == *.gz ]]; then
    gunzip -c "$dump" | docker exec -e MYSQL_HOST=127.0.0.1 -e MYSQL_UNIX_PORT= -i "$container" mysql \
      -h127.0.0.1 \
      -uroot -p"$MYSQL_ROOT_PASSWORD" \
      --init-command="SET SESSION sql_mode=''" \
      --force \
      "$MYSQL_DATABASE"
  else
    docker exec -e MYSQL_HOST=127.0.0.1 -e MYSQL_UNIX_PORT= -i "$container" mysql \
      -h127.0.0.1 \
      -uroot -p"$MYSQL_ROOT_PASSWORD" \
      --init-command="SET SESSION sql_mode=''" \
      --force \
      "$MYSQL_DATABASE" < "$dump"
  fi
}

print_version() {
  local container="$1"
  mysql_root "$container" -Nse "SELECT VERSION();" 2>/dev/null \
    || mysql_local "$container" mysql -h127.0.0.1 -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -Nse "SELECT VERSION();"
}

container_image() {
  docker inspect "$1" --format '{{.Config.Image}}' 2>/dev/null || echo ""
}

assert_stage_is_upgrade() {
  local version image
  version="$(print_version "$STAGE_CONTAINER")"
  image="$(container_image "$STAGE_CONTAINER")"
  echo "Stage image: ${image}  version: ${version}"
  if [[ "$version" == 5.7* ]] || [[ "$image" == *5.7* ]]; then
    echo "Stage is still MySQL 5.7 (${image} / ${version}). Not a cutover target." >&2
    echo "Check .env / .env.prod for MYSQL_CUTOVER_IMAGE, then:" >&2
    echo "  MYSQL_CUTOVER_IMAGE=mysql:8.0 FORCE=1 $0 stage" >&2
    exit 1
  fi
}

cmd_stage() {
  require_live_db
  assert_has_data "$LIVE_CONTAINER" "live" || exit 1
  if [[ -e "$STAGE_DATADIR" ]] && [[ -n "$(ls -A "$STAGE_DATADIR" 2>/dev/null || true)" ]]; then
    if [[ "${FORCE:-}" != "1" ]]; then
      echo "${STAGE_DATADIR} already has files. Refusing to reuse it." >&2
      echo "Move it aside, or rerun with FORCE=1 to destroy ./db8 only (never ./db)." >&2
      exit 1
    fi
    echo "FORCE=1: removing staging container and ${STAGE_DATADIR} (not ./db)"
    compose_stage stop db8 >/dev/null 2>&1 || true
    compose_stage rm -f db8 >/dev/null 2>&1 || true
    docker rm -f "$STAGE_CONTAINER" >/dev/null 2>&1 || true
    # Files are uid 999 (mysql). Host ubuntu cannot rm them.
    if [[ -e "$STAGE_DATADIR" ]]; then
      docker run --rm -v "$(dirname "$STAGE_DATADIR"):/parent" alpine:3.20 \
        rm -rf "/parent/$(basename "$STAGE_DATADIR")"
    fi
  fi
  mkdir -p "$STAGE_DATADIR"

  local stamp
  stamp="$(date +%Y-%m-%d-%H%M%S)"
  local dump="${DUMP_DIR}/foreverland-cutover-stage-${stamp}.sql.gz"
  dump_live "$dump"

  echo "Starting ${STAGE_CONTAINER} (${MYSQL_CUTOVER_IMAGE}) on ${STAGE_DATADIR} ..."
  compose_stage up -d --force-recreate --no-deps db8
  wait_for_mysql "$STAGE_CONTAINER"
  assert_stage_is_upgrade
  restore_dump "$dump" "$STAGE_CONTAINER"
  assert_has_data "$STAGE_CONTAINER" "staged restore" || exit 1

  echo
  echo "Staged ${MYSQL_CUTOVER_IMAGE}: $(print_version "$STAGE_CONTAINER")"
  echo "Live still serving from ./db: $(print_version "$LIVE_CONTAINER")"
  echo "Dump kept at ${dump}"
  echo "Next: CUTOVER=1 $0 cutover"
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
      summarize_db "$LIVE_CONTAINER" || true
    fi
  else
    echo "Live ${LIVE_CONTAINER}: not created"
  fi
  if docker ps -a --format '{{.Names}} {{.Status}}' | grep -q "^${STAGE_CONTAINER} "; then
    echo -n "Stage ${STAGE_CONTAINER}: "
    docker ps -a --format '{{.Names}} {{.Status}}' | grep "^${STAGE_CONTAINER} "
    if docker ps --format '{{.Names}}' | grep -q "^${STAGE_CONTAINER}$"; then
      echo "  version $(print_version "$STAGE_CONTAINER")"
      summarize_db "$STAGE_CONTAINER" || true
    fi
  else
    echo "Stage ${STAGE_CONTAINER}: not created"
  fi
  ls -ld "$LIVE_DATADIR" "$STAGE_DATADIR" 2>/dev/null || true
  ls -d "${REPO_ROOT}"/db57-backup-* 2>/dev/null || true
  ls -lh "${DUMP_DIR}"/foreverland-cutover-*.sql.gz 2>/dev/null || true
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

cmd_import_dump() {
  require_live_db
  local dump="${1:-}"
  if [[ -z "$dump" ]]; then
    dump="$(ls -1t "${DUMP_DIR}"/foreverland-cutover-final-*.sql.gz 2>/dev/null | head -n 1 || true)"
  fi
  if [[ -z "$dump" || ! -f "$dump" ]]; then
    echo "No dump file. Pass a path or keep one in ${DUMP_DIR}/foreverland-cutover-final-*.sql.gz" >&2
    exit 1
  fi
  restore_dump "$dump" "$LIVE_CONTAINER"
  assert_has_data "$LIVE_CONTAINER" "import-dump" || exit 1
  echo "Import complete."
}

cmd_cutover() {
  if [[ "${CUTOVER:-}" != "1" ]]; then
    echo "Refusing cutover without CUTOVER=1 (this stops web and swaps ./db)." >&2
    exit 1
  fi
  require_live_db
  assert_has_data "$LIVE_CONTAINER" "live before cutover" || exit 1
  if [[ ! -d "$STAGE_DATADIR" ]] || [[ -z "$(ls -A "$STAGE_DATADIR" 2>/dev/null || true)" ]]; then
    echo "No staged ./db8. Run $0 stage first." >&2
    exit 1
  fi
  if ! docker ps --format '{{.Names}}' | grep -q "^${STAGE_CONTAINER}$"; then
    echo "${STAGE_CONTAINER} is not running. Run $0 stage first." >&2
    exit 1
  fi
  assert_stage_is_upgrade
  assert_has_data "$STAGE_CONTAINER" "staged before cutover" || exit 1

  echo "Stopping web so nothing writes to 5.7 ..."
  docker stop foreverland >/dev/null

  local stamp
  stamp="$(date +%Y-%m-%d-%H%M%S)"
  local dump="${DUMP_DIR}/foreverland-cutover-final-${stamp}.sql.gz"
  dump_live "$dump"
  restore_dump "$dump" "$STAGE_CONTAINER"
  assert_has_data "$STAGE_CONTAINER" "staged after final restore" || exit 1

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

  echo "Starting cut-over db (force-recreate) ..."
  compose up -d --force-recreate --no-deps db
  wait_for_mysql "$LIVE_CONTAINER"
  echo "Now running $(print_version "$LIVE_CONTAINER")"
  if ! assert_has_data "$LIVE_CONTAINER" "live after swap"; then
    echo "Post-swap database is empty. Rolling back automatically." >&2
    ROLLBACK=1 cmd_rollback
    exit 1
  fi
  compose up -d --no-deps web

  echo
  echo "Cutover complete. 5.7 files are in ${backup} — keep them for a week."
  echo "Cutover complete. Keep ${backup} until you are ready to delete it."
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
  compose up -d --force-recreate --no-deps db
  wait_for_mysql "$LIVE_CONTAINER"
  echo "Restored $(print_version "$LIVE_CONTAINER")"
  summarize_db "$LIVE_CONTAINER" || true
  compose up -d --no-deps web
  echo "Rollback complete. Web is on mysql:5.7 + ./db again."
}

if [[ $# -lt 1 ]]; then
  usage
fi

load_env_prod
case "$1" in
  stage) cmd_stage ;;
  status) cmd_status ;;
  cutover) cmd_cutover ;;
  rollback) cmd_rollback ;;
  import-dump) shift; cmd_import_dump "${1:-}" ;;
  *) usage ;;
esac
