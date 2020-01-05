
from rest_framework import serializers
from .models import Student


class StudentSerializerNameAndUid(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 2
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
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