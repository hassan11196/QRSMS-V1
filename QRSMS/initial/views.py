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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.forms.models import model_to_dict
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

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

def check_if_admin(user):
    return True if user.is_staff else False

class UserNotLogged(View):

    def get(self, request):
        return JsonResponse({'message':'Not Authenticated'}, status=401)

class Add_students(View):
     permission_classes = [IsAdminUser]
     def post(self, request):
        print('Inserting Students')
        from .root_commands import insert_students
        
        data = model_to_dict(insert_students())
        return JsonResponse({'status':'success', **data})


class Add_semesterCore(View):
    @method_decorator(user_passes_test(check_if_admin,login_url='/management/user_not_logged/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



    def post(self, request):
        print('Inserting Semester')
        from .root_commands import add_semesterCore
        data = model_to_dict(add_semesterCore())
        return JsonResponse({'status':'success', **data})     
    
    
    
    
        
class Add_university(View):
    def post(self, request):
        print('Inserting University')
        from .root_commands import add_university
        data = model_to_dict(add_university())
        return JsonResponse({'status':'success', **data})    

class Add_superuser(View):
    def post(self, request):
        print('Inserting Superusers')
        from .root_commands import create_super_users
        data = model_to_dict(create_super_users())
        return JsonResponse({'status':'success', **data})    


        

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

