from django.contrib.auth.models import Group
from rest_framework import serializers
from . import models


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['user', 'nu_email']
