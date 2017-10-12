# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('ID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Prof',
            fields=[
                ('profid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('office', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('course', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('Name', models.CharField(max_length=200)),
                ('Roll_Number', models.AutoField(primary_key=True, serialize=False)),
                ('Semester', models.IntegerField()),
                ('Degree', models.CharField(max_length=20)),
                ('Department', models.CharField(max_length=25)),
                ('Email', models.EmailField(max_length=254)),
            ],
        ),
    ]
