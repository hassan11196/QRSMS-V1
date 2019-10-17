from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from .models import User, Teacher, Faculty, Student, Semester, Course, RegularCoreCourseLoad
from django_restful_admin import site
# Register your models here.


class NewUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class NewUserCreationForm(UserCreationForm):

    cnic2 = forms.IntegerField(validators=[RegexValidator("[0-9]{5}-[0-9]{7}-[0-9]{1}")])
    class Meta(UserCreationForm.Meta):
        model = User
        field_classes = {'cnic':'cnic'}
        

class NewUserAdmin(UserAdmin):
    # form = NewUserChangeForm
    # form = NewUserCreationForm
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                ('gender',),
                ('CNIC',),
                ('is_student',),
                ('is_teacher',),
                ('is_faculty',),
                ('is_maintainer',)
            )
        }
        ),
    )


# class CourseAdminForm(forms.ModelForm):

#     class Meta:
#         model = Course
#         fields = '__all__'


# class CourseAdmin(admin.ModelAdmin):
#     form = CourseAdminForm
#     list_display = ['course_name', 'course_code']
#     readonly_fields = ['course_name', 'course_code']

# admin.site.register(Course, CourseAdmin)









admin.site.register(RegularCoreCourseLoad)
admin.site.register(User, NewUserAdmin)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Semester)

site.register(User)
site.register(Teacher)
site.register(Faculty)
site.register(Student)
site.register(Semester)
site.register(RegularCoreCourseLoad)