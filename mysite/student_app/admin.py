# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from student_app.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(User)
# Register your models here.
