from django.contrib import admin
from .models import University,Campus,Department,Degree
from django_restful_admin import site
# Register your models here.

admin.site.register(University)
admin.site.register(Campus)
admin.site.register(Department)
admin.site.register(Degree)


site.register(University)
site.register(Campus)
site.register(Department)
site.register(Degree)