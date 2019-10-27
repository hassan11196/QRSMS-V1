from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
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

# Create your views here.

from .forms import FacultyForm
from .models import  Faculty

class FacultyListView(ListView):
    model = Faculty


class FacultyCreateView(CreateView):
    model = Faculty
    form_class = FacultyForm


class FacultyDetailView(DetailView):
    model = Faculty


class FacultyUpdateView(UpdateView):
    model = Faculty
    form_class = FacultyForm
