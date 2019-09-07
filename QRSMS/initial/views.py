from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

from django.shortcuts import render,HttpResponse

# Create your views here.
def index(response):
    return HttpResponse('Initital App'  + '<br>' + str(type(response)) + '<br>' + str(dir(response))  +  '<br>' + str(response.get_host) + '<br>' + str(response.is_secure))

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer