from django.contrib.auth.models import Group
from .models import Faculty
from rest_framework import serializers
from . import models



class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Faculty
        fields = '__all__'
