from . import models
from . import serializers
from rest_framework import viewsets, permissions, routers


class EmployeeViewSet(viewsets.ModelViewSet):
    model = models.Employee
