# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.

from .models import Students, Courses, Prof, Enrollment
# users = User.objects.all()
# admin.site.register(users)
admin.site.register(Students)
admin.site.register(Courses)
admin.site.register(Prof)
admin.site.register(Enrollment)
