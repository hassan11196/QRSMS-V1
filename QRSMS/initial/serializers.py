
from .models import Course, RegularCoreCourseLoad, RegularElectiveCourseLoad, OfferedCourses, CourseStatus, MarkSheet, AttendanceSheet
from rest_framework import serializers
from . import models


class AttendanceSheetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AttendanceSheet
        fields = '__all__'
        depth = 1


class OfferedCoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferedCourses
        fields = ('courses_offered','semester_code') 
        depth = 2
    


class CourseStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseStatus
        fields = '__all__'


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class RegularCoreCourseLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model= RegularCoreCourseLoad
        fields = '__all__'
        depth = 1

class RegularElectiveCourseLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model= RegularElectiveCourseLoad
        fields = '__all__'
        depth = 3
# class StudentSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['arn','uid','user']




# class CourseSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.Course
#         fields = (
#             'pk', 
#             'course_name', 
#             'course_code', 
#         )


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Teacher
        fields = (
            'pk', 
            'department', 
            'nu_email', 
        )


class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Faculty
        fields = (
            'pk', 
        )


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Student
        fields = (
            'pk', 
            'batch', 
            'arn', 
            'uid', 
            'degree_name_enrolled', 
            'degree_short_enrolled', 
            'department_name_enrolled', 
            'uni_mail', 
        )


class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Semester
        fields = [
            'pk', 
            # 'semester_year', 
            # 'start_date', 
            # 'end_date', 
        ]



