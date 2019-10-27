from django.contrib import admin
from django_restful_admin import site
from .models import Teacher
# Register your models here.

admin.site.register(Teacher)

site.register(Teacher)