"""Record migrations that only describe tables already present in a prod dump.

Yesterday's queryset work added Django 4 initials for members/shows/songs/
marketing/media. Older dumps already have those tables (South created them)
and already have fidouche.0001_initial applied. That migration depends on
members/shows first migrations, so `migrate` and `migrate --fake-initial`
both fail the history check before they can fake anything.

This command writes django_migrations rows directly. It does not change
schema. Run it, then `migrate` for real pending changes (e.g. fidouche.0005
payment method columns).
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


# (app, migration name, table that must already exist)
TABLE_ALREADY_THERE = (
    ("members", "0001_initial", "members_member"),
    ("shows", "0001_initial", "shows_show"),
    ("songs", "0001_initial", "songs_song"),
    ("marketing", "0001_initial", "marketing_testimonial"),
    ("media", "0001_initial", "media_album"),
    ("media", "0002_initial", "media_album_show"),
    ("thumbnail", "0001_initial", "thumbnail_kvstore"),
)

# (app, migration name, table, column)
COLUMN_ALREADY_THERE = (
    ("marketing", "0002_initial", "marketing_testimonial", "show_id"),
)

# AlterField-only fidouche follow-ups. Safe to record once 0002 is applied
# and the table exists. Do not include 0005 (adds payment method columns).
FIDOUCHE_ALTERS = (
    "0003_auto_20201021_0956",
    "0004_auto_20210304_1045",
)


class Command(BaseCommand):
    help = (
        "Fake-apply initials for apps whose tables already exist so migrate "
        "can run after a prod dump. Does not change schema."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be recorded without writing.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        recorder = MigrationRecorder(connection)
        recorder.ensure_schema()
        applied = {(m.app, m.name) for m in recorder.migration_qs.all()}
        tables = set(connection.introspection.table_names())
        recorded = []

        def record(app, name, reason):
            key = (app, name)
            if key in applied:
                return
            self.stdout.write(f"  record {app}.{name}  ({reason})")
            if not dry_run:
                recorder.record_applied(app, name)
            applied.add(key)
            recorded.append(key)

        self.stdout.write("Checking tables that predate the new initials…")
        for app, name, table in TABLE_ALREADY_THERE:
            if table in tables:
                record(app, name, f"{table} exists")

        for app, name, table, column in COLUMN_ALREADY_THERE:
            if table in tables and _has_column(table, column):
                record(app, name, f"{table}.{column} exists")

        if ("fidouche", "0002_fiduciary_fiduciarypayment") in applied:
            if "fidouche_expense" in tables:
                for name in FIDOUCHE_ALTERS:
                    record("fidouche", name, "alter-only; table already matches")

        if not recorded:
            self.stdout.write("Nothing to record. History already matches the dump.")
        elif dry_run:
            self.stdout.write(self.style.WARNING(f"Dry run: {len(recorded)} would be recorded."))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Recorded {len(recorded)} migration(s). Next: python manage.py migrate"
                )
            )


def _has_column(table, column):
    with connection.cursor() as cursor:
        description = connection.introspection.get_table_description(cursor, table)
    return any(col.name == column for col in description)
