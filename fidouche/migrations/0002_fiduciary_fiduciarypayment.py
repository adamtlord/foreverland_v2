# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2019-06-20 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '__first__'),
        ('fidouche', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fiduciary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', localflavor.us.models.USStateField(blank=True, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Zip')),
                ('phone', localflavor.us.models.PhoneNumberField(blank=True, null=True)),
                ('ssn', models.CharField(blank=True, max_length=16, null=True, verbose_name=b'SSN/EIN')),
            ],
            options={
                'verbose_name_plural': 'Fiduciaries',
            },
        ),
        migrations.CreateModel(
            name='FiduciaryPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('check_no', models.IntegerField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('fidouche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fiduciary_payment', to='fidouche.Fiduciary')),
                ('show', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fiduciary_payment', to='shows.Show')),
            ],
            options={
                'ordering': ['show__date'],
            },
        ),
    ]