from . import models
from . import serializers
from rest_framework import viewsets, permissions, routers


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Student class"""

    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
