from django.db import migrations

import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ("fidouche", "0005_auto_20210714_1224"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payee",
            name="ssn",
            field=common.fields.EncryptedCharField(
                blank=True, max_length=255, null=True, verbose_name="SSN#"
            ),
        ),
        migrations.AlterField(
            model_name="agent",
            name="ssn",
            field=common.fields.EncryptedCharField(
                blank=True, max_length=255, null=True, verbose_name="SSN/EIN"
            ),
        ),
        migrations.AlterField(
            model_name="productioncompany",
            name="ssn",
            field=common.fields.EncryptedCharField(
                blank=True, max_length=255, null=True, verbose_name="SSN/EIN"
            ),
        ),
        migrations.AlterField(
            model_name="fiduciary",
            name="ssn",
            field=common.fields.EncryptedCharField(
                blank=True, max_length=255, null=True, verbose_name="SSN/EIN"
            ),
        ),
    ]
