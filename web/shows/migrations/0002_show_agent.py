from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fidouche", "0005_auto_20210714_1224"),
        ("shows", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
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
