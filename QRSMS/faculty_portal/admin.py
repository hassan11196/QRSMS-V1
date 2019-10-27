from django.contrib import admin
from django_restful_admin import site
from .models import Faculty
# Register your models here.

admin.site.register(Faculty)

site.register(Faculty)