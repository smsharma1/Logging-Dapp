# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Prof, Students, Courses
# Register your models here.

admin.site.register(Prof)
admin.site.register(Students)
admin.site.register(Courses)