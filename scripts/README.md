# Database dump / load

Use the shell scripts to copy production data into your local dev database. No Fabric or Django required to run them.

## 1. Dump prod DB

**On the machine where the prod DB runs** (e.g. prod server, or locally with prod stack up):

- Have `.env.prod` in the repo root with `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`.
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

- Have `.env` in the repo root (dev DB credentials).
- Run from repo root:
  ```bash
  ./scripts/load-dump-into-dev.sh data/dumps/foreverland-dump-YYYY-MM-DD-HHMMSS.sql.gz
  ```
- The script drops the existing dev database, recreates it, and loads the dump. Uncompressed `.sql` files work too.

Make sure the scripts are executable: `chmod +x scripts/dump-prod-db.sh scripts/load-dump-into-dev.sh`
