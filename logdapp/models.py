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
    course = models.CharField(max_length=20)

class Students(models.Model):
    Name = models.CharField(max_length = 200)
    Roll_Number = models.AutoField(primary_key=True)
    Semester = models.IntegerField()
    Degree = models.CharField(max_length = 20)
    Department = models.CharField(max_length = 25)
    Email = models.EmailField()

class Courses(models.Model):
    ID = models.CharField(max_length=10,primary_key=True)
    Name = models.CharField(max_length=20)

class Enrollment(models.Model):
    Course_ID = models.ForeignKey(Courses)
    Student_ID = models.ForeignKey(Students)
    Prof_ID = models.ForeignKey(Prof)
    Grade = models.CharField(max_length=2)


