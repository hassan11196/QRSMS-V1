from django.contrib.auth.models import User, Group
from .models import course
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = ['course_name','course_code','course_short']