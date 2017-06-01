# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-01 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '__first__'),
        ('songs', '0004_auto_20170601_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='setsong',
            name='transition',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='song',
            name='bpm',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='solos',
            field=models.ManyToManyField(blank=True, related_name='soloist', to='members.Member'),
        ),
    ]
