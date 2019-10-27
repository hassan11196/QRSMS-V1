from django.contrib import admin
from .models import Student
from django_restful_admin import site
# Register your models here.
admin.site.register(Student)

site.register(Student)