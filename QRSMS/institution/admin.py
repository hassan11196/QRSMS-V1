from django.contrib import admin
from .models import University,Campus,Department,Degree,BatchSection
from django_restful_admin import site
# Register your models here.

admin.site.register(University)
admin.site.register(Campus)
admin.site.register(Department)
admin.site.register(Degree)
admin.site.register(BatchSection)


site.register(University)
site.register(Campus)
site.register(Department)
site.register(Degree)
site.register(BatchSection)

