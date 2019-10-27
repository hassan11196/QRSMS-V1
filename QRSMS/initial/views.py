from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from rest_framework import generics, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.views.generic import DetailView, ListView, UpdateView, CreateView


from .serializers import (CourseSerializer)


from .forms import CourseForm, SemesterForm
from .models import Course, Semester

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

# @login_required(login_url ='/')
def ping(request):
    return JsonResponse({'result': 'OK'})


def index(request):
    return render(request, 'initial/index.html')


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseListView(ListView):
    model = Course


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm


class CourseDetailView(DetailView):
    model = Course


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm


class SemesterListView(ListView):
    model = Semester


class SemesterCreateView(CreateView):
    model = Semester
    form_class = SemesterForm


class SemesterDetailView(DetailView):
    model = Semester


class SemesterUpdateView(UpdateView):
    model = Semester
    form_class = SemesterForm

