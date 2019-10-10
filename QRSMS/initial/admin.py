from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.core.validators import RegexValidator
from .models import User, Teacher, Faculty, Student, Semester, Course
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


class CourseAdminForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ['course_name', 'course_code']
    readonly_fields = ['course_name', 'course_code']

admin.site.register(Course, CourseAdmin)


class TeacherAdminForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = ['department', 'nu_email']
    readonly_fields = ['department', 'nu_email']

admin.site.register(Teacher, TeacherAdmin)


class FacultyAdminForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = '__all__'


class FacultyAdmin(admin.ModelAdmin):
    form = FacultyAdminForm


admin.site.register(Faculty, FacultyAdmin)


class StudentAdminForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'


class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ['batch', 'arn', 'uid', 'degree_name_enrolled', 'degree_short_enrolled', 'department_name_enrolled', 'uni_mail']
    readonly_fields = ['batch', 'arn', 'uid', 'degree_name_enrolled', 'degree_short_enrolled', 'department_name_enrolled', 'uni_mail']

admin.site.register(Student, StudentAdmin)


# class SemesterAdminForm(forms.ModelForm):

#     class Meta:
#         model = Semester
#         fields = '__all__'


# class SemesterAdmin(admin.ModelAdmin):
#     form = SemesterAdminForm
#     list_display = ['semester_year', 'start_date', 'end_date']
#     readonly_fields = ['semester_year', 'start_date', 'end_date']

# admin.site.register(Semester, SemesterAdmin)




admin.site.register(User, NewUserAdmin)
# admin.site.register(Teacher)
# admin.site.register(Faculty)
# admin.site.register(Student)
# admin.site.register(Semester)

site.register(User)
site.register(Teacher)
site.register(Faculty)
site.register(Student)
site.register(Semester)