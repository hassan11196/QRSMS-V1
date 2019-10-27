from django import forms
from .models import Course, Semester


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code']


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = [ 'teachers_available','semester_year', 'start_date', 'end_date']

