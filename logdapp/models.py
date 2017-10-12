# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Prof(models.Model):
    profid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    office = models.CharField(max_length=200)
    email = models.EmailField()
    course = models.CharField(max_length=200)