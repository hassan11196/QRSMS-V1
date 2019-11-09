
"""
Admin
"""
from django.contrib import admin
from django_restful_admin import site
from .models import Semester, Course, RegularCoreCourseLoad, RegularElectiveCourseLoad, CourseClass, CourseSection, Attendance, RepeatCourseLoad



admin.site.register(RegularCoreCourseLoad)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(RegularElectiveCourseLoad)
admin.site.register(CourseClass)
admin.site.register(CourseSection)
admin.site.register(Attendance)
admin.site.register(RepeatCourseLoad)

site.register(RepeatCourseLoad)
site.register(RegularElectiveCourseLoad)
site.register(Semester)
site.register(RegularCoreCourseLoad)
site.register(Course)
site.register(CourseClass)
site.register(CourseSection)
site.register(Attendance)