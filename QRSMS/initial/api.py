from . import models
from . import serializers
from rest_framework import viewsets, permissions, routers


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for the Course class"""

    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    """ViewSet for the Teacher class"""

    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]


class FacultyViewSet(viewsets.ModelViewSet):
    """ViewSet for the Faculty class"""

    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Student class"""

    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SemesterViewSet(viewsets.ModelViewSet):
    """ViewSet for the Semester class"""

    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [permissions.IsAuthenticated]


