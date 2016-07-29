# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-29 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokewatcher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.DecimalField(decimal_places=14, max_digits=16),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(decimal_places=14, max_digits=16),
        ),
    ]