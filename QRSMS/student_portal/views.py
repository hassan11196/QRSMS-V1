from django.contrib.auth import authenticate, login,logout
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
from django.utils.decorators import method_decorator


from .serializers import StudentSerializer


from .forms import StudentForm, StudentFormValidate
from .models import Student
# Create your views here.


class Home_json(View):
        
    def get(self, request):
        print(dir(request))
        data_dict = model_to_dict(Student.objects.filter(uid = request.user).first())
        user_data = model_to_dict(request.user)
        print(data_dict)
        print(user_data)
        dat = {'status':'success',**data_dict,**user_data}
        
        return JsonResponse(dat)
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        

class StudentSignupView(View):
    def post(self, request):
        form = StudentFormValidate(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return JsonResponse({'status':"Success", 'message':'Student Sign Up Successful.'})
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
            dict_user = model_to_dict(user)
            return JsonResponse({'status':'success','message' : 'User Logged In', **dict_user})
        else:
            return JsonResponse({'status':"Invalid Username of Password."}, status = 403)
        
        return HttpResponseRedirect('/home')

class StudentLogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'status':'success','message' : 'User Logged Out'})

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


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


