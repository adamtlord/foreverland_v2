from django.db import migrations, models
import django.db.models.deletion


class AddFieldIfMissing(migrations.AddField):
    """Prod dumps already have shows_show.agent_id from South. Tests do not."""

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.model_name)
        table = model._meta.db_table
        with schema_editor.connection.cursor() as cursor:
            existing = {
                col.name
                for col in schema_editor.connection.introspection.get_table_description(
                    cursor, table
                )
            }
        if "agent_id" in existing:
            return
        super().database_forwards(app_label, schema_editor, from_state, to_state)


class Migration(migrations.Migration):

    dependencies = [
        ("fidouche", "0005_auto_20210714_1224"),
        ("shows", "0001_initial"),
    ]

    operations = [
        AddFieldIfMissing(
            model_name="show",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="gig_agent",
                to="fidouche.agent",
            ),
        ),
    ]
