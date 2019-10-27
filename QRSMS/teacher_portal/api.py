from . import models
from . import serializers
from rest_framework import viewsets, permissions, routers


class TeacherViewSet(viewsets.ModelViewSet):
    """ViewSet for the Teacher class"""

    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
