
from rest_framework import serializers
from .models import Student
from actor.models import User


def WrapperStudentSerializer(*args):
    class StudentSerializerCustom(serializers.ModelSerializer):
        class Meta:
            model = Student
            fields = args

    return StudentSerializerCustom()


class UserSerializerOnlyName(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class StudentSerializerAllData(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 2


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


# class RegisterStudent(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ["degree_name_enrolled"]


class StudentSerializerOnlyNameAndUid(serializers.ModelSerializer):

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
