from . import models
from . import serializers
from rest_framework import viewsets, permissions, routers

class FacultyViewSet(viewsets.ModelViewSet):
    """ViewSet for the Faculty class"""

    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [permissions.IsAuthenticated]

