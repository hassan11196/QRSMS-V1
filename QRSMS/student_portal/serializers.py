
from rest_framework import serializers
from .models import Student
from actor.models import User

class UserSerializerOnlyName(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
class StudentSerializerNameAndUid(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 2
class StudentSerializer(serializers.ModelSerializer):
    
    user = UserSerializerOnlyName()
    class Meta:
        model = Student
        fields = (
            'batch', 
            'uid', 
            'degree_short_enrolled', 
            'uni_mail', 
            'user'
        )