from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Teacher, Faculty, Student, Semester
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Teacher)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Semester)