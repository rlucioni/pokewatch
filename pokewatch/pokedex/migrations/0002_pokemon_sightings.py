# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 23:10
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='sightings',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]
