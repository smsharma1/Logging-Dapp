# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logdapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prof',
            name='course',
            field=models.CharField(max_length=20),
        ),
    ]
