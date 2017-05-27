# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 16:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SetSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='songs.Set')),
                ('song', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='songs.Song')),
            ],
        ),
        migrations.RemoveField(
            model_name='setlistsong',
            name='setlist',
        ),
        migrations.RemoveField(
            model_name='setlistsong',
            name='song',
        ),
        migrations.RemoveField(
            model_name='setlist',
            name='songs',
        ),
        migrations.DeleteModel(
            name='SetlistSong',
        ),
        migrations.AddField(
            model_name='set',
            name='setlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='songs.Setlist'),
        ),
        migrations.AddField(
            model_name='set',
            name='songs',
            field=models.ManyToManyField(through='songs.SetSong', to='songs.Song'),
        ),
    ]
