from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.middleware.csrf import get_token
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from rest_framework import generics, viewsets
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema

from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator



import re
import openpyxl
from initial.root_commands import add_semesterCore
from .serializers import FacultySerializer
from initial.serializers import SemesterSerializer
# Create your views here.

from .forms import FacultyForm
from .models import  Faculty

def check_if_faculty(user):
    return True if user.is_faculty else False

class BaseFacultyLoginView(APIView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_if_faculty, login_url='/faculty/login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class SemesterStart(BaseFacultyLoginView):

    @swagger_auto_schema(request_body=SemesterSerializer)
    def post(self, request, format=None):
        print(request.data)
        # add_semesterCore('Spring2020', semester_season, semester_year, start_date, end_date)
        return Response(request.data)

    def delete(self, request, format=None):
        return Response('Delete Api - Debug')

class Home_json(BaseFacultyLoginView):
        
    def get(self, request):
        print(dir(request))
        fa = Faculty.objects.filter(user__username = str(request.user))
        faculty_data = FacultySerializer(fa, many=True,  context={'request': Request(request)}).data
        dat = {'status':'success', 'message':'Faculty Data', 'data':faculty_data}
        
        return JsonResponse(dat)

class FacultyLoginView(View):

    def get(self, request,*args, **kwargs):
        return HttpResponse("PLease Login" + str(kwargs))

    def post(self, request,*args,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if username is "" or password is "":
            return HttpResponse(content="Empty Usename or Password Field.", status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            dict_user = model_to_dict(user)
            dict_user.pop('password')
            dict_user.pop('groups')
            return JsonResponse({'status':'success','message' : 'User Logged In', 'data':dict_user})
        else:
            return JsonResponse({'status':"Invalid Username of Password."}, status = 403)
        
        


class GetStudentTimeTable(BaseFacultyLoginView):

    def post(self, request):
        excel_file = request.FILES["student_timetable_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets

        student_batch = request.POST['batch']
        if student_batch == None:
            student_batch = 2016
        worksheet = wb["BATCH " + str(student_batch)]
        print(worksheet)

        excel_data = list()
        code = list()
        title = list()
        short = list()
        crdthr = list()
        section = list()
        instructor = list()
        for col in worksheet['C']:
            if(col.value != None):
                code.append(col.value)
        for col in worksheet['D']:
            if(col.value != None):
                title.append(col.value)
        for col in worksheet['E']:
            if(col.value != None):
                short.append(col.value)
        for col in worksheet['G']:
            if(col.value != None):
                crdthr.append(col.value)

        for col in worksheet['I']:
            if(col.value != None):
                col.value = col.value.replace(' ','')
                if(('CoursePlanning:' in col.value)or('Courseplanning:' in col.value)):
                    s = re.findall(r'[A-Za-z]+:[A-Z,a-z0-9()\/]+\)',col.value)[0]
                    col.value=col.value.replace(s,'')
                insArray = col.value
                secArray = re.findall(r'\([A-Za-z,0-9]*\)',col.value)
                subjSec = list()
                for sec in secArray:
                    insArray = insArray.replace(sec,'').replace(' ','')
                    sec=sec.replace('(','').replace(')','').split(',')
                    subjSec.append(sec)
                section.append(subjSec)
                insArray = insArray.split(',')
                instructor.append(insArray)
        
        timetable_list = []

        for i in range(1,len(code)):
            print(code[i])
            print(title[i])
            print(short[i]) 
            print(crdthr[i])
            print(instructor[i])
            print(section[i])
            timetable_list.append(
                {'course_code':code[i],
                'course_name':title[i],
                'course_short':short[i],
                'course_credits':crdthr[i],
                'course_instructors':instructor[i],
                'course_sections':section[i]
                }
            )


        return JsonResponse({'status':'success','message' : 'TimeTable', 'data': timetable_list})


class FacultyLogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'status':'success','message' : 'User Logged Out'})

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
