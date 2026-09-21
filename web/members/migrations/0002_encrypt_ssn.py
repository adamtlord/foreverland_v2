from django.db import migrations

import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="ssn",
            field=common.fields.EncryptedCharField(
                blank=True, max_length=255, null=True, verbose_name="SSN#"
            ),
        ),
        migrations.AlterField(
            model_name="sub",
            name="ssn",
            field=common.fields.EncryptedCharField(
                blank=True, max_length=255, null=True, verbose_name="SSN#"
            ),
        ),
    ]
