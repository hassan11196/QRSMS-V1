
from .models import Course, RegularCoreCourseLoad, RegularElectiveCourseLoad
from rest_framework import serializers
from . import models



class CourseSerializer(serializers.ModelSerializer):
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



