from django.contrib import admin
from .models import Student,FeeChallan
from django_restful_admin import site
# Register your models here.
admin.site.register(Student)
admin.site.register(FeeChallan)
site.register(Student)