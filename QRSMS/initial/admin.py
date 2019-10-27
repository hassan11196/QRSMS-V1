
"""
Admin
"""
from django.contrib import admin
from django_restful_admin import site
from .models import Semester, Course, RegularCoreCourseLoad



admin.site.register(RegularCoreCourseLoad)
admin.site.register(Course)
admin.site.register(Semester)

site.register(Semester)
site.register(RegularCoreCourseLoad)
site.register(Course)
