# Database dump / load

Use the shell scripts to copy production data into your local dev database. No Fabric or Django required to run them.

## 1. Dump prod DB

**On the machine where the prod DB runs** (e.g. prod server, or locally with prod stack up):

- Have `.env.prod` in the repo root with `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_ROOT_PASSWORD` (required for MySQL/MariaDB first-time init).
- Run:
  ```bash
  ./scripts/dump-prod-db.sh
  ```
- Writes `data/dumps/foreverland-dump-YYYY-MM-DD-HHMMSS.sql.gz`.
- To specify the output path: `./scripts/dump-prod-db.sh data/dumps/my-dump.sql.gz`

**From a remote prod server:** run the script there, then copy the file to your machine, e.g.:
```bash
scp user@prod-server:/path/to/foreverland_v2/data/dumps/foreverland-dump-*.sql.gz ./data/dumps/
```

## 2. Load dump into dev

**On your dev machine**, with the dev stack up (`docker compose up -d db` or full stack):

- Have `.env` in the repo root (dev DB credentials, including `MYSQL_ROOT_PASSWORD`).
- Dev DB container is `foreverland_db_dev` (override with `DEV_DB_CONTAINER`).
- Run from repo root:
  ```bash
  ./scripts/load-dump-into-dev.sh data/dumps/foreverland-dump-YYYY-MM-DD-HHMMSS.sql.gz
  ```
- The script drops the existing dev database, recreates it, and loads the dump. Uncompressed `.sql` files work too.

Make sure the scripts are executable: `chmod +x scripts/dump-prod-db.sh scripts/load-dump-into-dev.sh scripts/deploy-prod.sh scripts/cutover-mysql.sh`

## MySQL 5.7 → 8 / MariaDB 10.11 cutover

Do this on the Ubuntu prod host after Django 4.2 is already running against 5.7 via `foreverland.mysql57`. The script never deletes `./db`.

```bash
# 1. Copy 5.7 into a new ./db8 and start foreverland_db8 (site stays on 5.7)
./scripts/cutover-mysql.sh stage
./scripts/cutover-mysql.sh status

# Optional: MYSQL_CUTOVER_IMAGE=mariadb:10.11 FORCE=1 ./scripts/cutover-mysql.sh stage

# 2. After you have checked finance totals against the staged DB:
CUTOVER=1 ./scripts/cutover-mysql.sh cutover

# 3. If the new server is wrong or empty:
ROLLBACK=1 ./scripts/cutover-mysql.sh rollback
```

If live is empty after cutover, do not keep serving MySQL 8. The 5.7 files are in `./db57-backup-*`. Rollback puts those back and force-recreates `mysql:5.7`. To stay on 8 instead, only if a cutover dump is large and contains `INSERT` rows:

```bash
./scripts/cutover-mysql.sh import-dump data/dumps/foreverland-cutover-final-YYYY-MM-DD-HHMMSS.sql.gz
```

`cutover` stops web, takes a final dump, restores it, renames `./db` → `./db57-backup-TIMESTAMP`, promotes `./db8` → `./db`, sets `PROD_DB_IMAGE` in `.env.prod`, and starts db+web. Keep the backup directory for a week. Then switch `ENGINE` to `django.db.backends.mysql` and delete `web/foreverland/mysql57/`.

## Production deploy

On the Ubuntu host, **always** use `docker-compose.prod.yml`. A bare `docker compose up` starts the **dev** file (`mariadb:10.6`, no nginx). That used to replace containers named `foreverland` / `foreverland_db` and leave nginx/certbot as orphans. Dev compose now uses project `foreverland-dev` and `*_dev` container names so it cannot clobber those.

Do **not** pass `--remove-orphans` unless you intend to delete nginx/certbot (TLS).

```bash
cd app   # repo root on the host
./scripts/deploy-prod.sh down
./scripts/deploy-prod.sh up -d --build --force-recreate
```

Equivalent without the script:

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build --force-recreate
```

Then confirm:

```bash
./scripts/deploy-prod.sh config
docker inspect foreverland_db --format '{{.Config.Image}} {{json .Mounts}}'
```

The db image must match `PROD_DB_IMAGE` in `.env.prod` (`mysql:5.7` until cutover; `mysql:8.0` or `mariadb:10.11` after). Mounts must include host `./db` → `/var/lib/mysql`. `MYSQL_PASSWORD` (app user) is not enough; first-time init needs `MYSQL_ROOT_PASSWORD`.

### Recover from a mistaken `docker compose up` (no `-f`)

Prod data lives in `./db` on the host. The default compose file does **not** mount that directory, so an empty MariaDB datadir does not mean the MySQL files are gone.

```bash
docker stop foreverland foreverland_db
docker rm foreverland foreverland_db
ls ./db    # should still contain MySQL files (ibdata1, mysql/, etc.)
./scripts/deploy-prod.sh up -d --build --force-recreate
```

Do not `docker volume prune`, and do not delete `./db`.
