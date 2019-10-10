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

from django.views.generic import DetailView, ListView, UpdateView, CreateView


from .serializers import (
    CourseSerializer, GroupSerializer, TeacherSerializer, UserSerializer, StudentSerializer)


from .forms import CourseForm, TeacherForm, FacultyForm, StudentForm, SemesterForm, StudentFormValidate
from .models import Course, Teacher, User,Student, Semester, Faculty
def temp_login(request):
    print(request)
    return HttpResponse("USer" + str(request.user))


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

# @login_required(login_url ='/')
def ping(request):
    return JsonResponse({'result': 'OK'})


def index(request):
    return render(request, 'initial/index.html')

class StudentSignupView(View):
    def post(self, request):
        form = StudentFormValidate(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return JsonResponse({'status':"Success"})
        else:
            return JsonResponse(form.errors.get_json_data())

class StudentLoginView(View):

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
            print(kwargs)
            print(args)
            print(request.build_absolute_uri())
            return HttpResponse('success', status=200)
        else:
            return HttpResponse("Invalid Username of Password.", status = 403)
        
        return HttpResponse("success" + str(user))


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


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


class TeacherListView(ListView):
    model = Teacher


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm


class TeacherDetailView(DetailView):
    model = Teacher


class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm


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


class StudentListView(ListView):
    model = Student


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm


class StudentDetailView(DetailView):
    model = Student


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm


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

