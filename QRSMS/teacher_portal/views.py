from django.contrib.auth import authenticate, login, logout
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
from django.contrib.auth.decorators import user_passes_test, login_required
from django.dispatch import receiver

from initial.models import CourseSection, SectionAttendance, Course, StudentAttendance
from .serializers import (TeacherSerializer)
from .signals import attendance_of_day_for_student

from .forms import  TeacherForm
from .models import  Teacher


def check_if_teacher(user):
    return True if user.is_teacher else False

# Create your views here.

# class TeacherSignupView(View):
#     def post(self, request):
#         form = TeacherFormValidate(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return JsonResponse({'status':"Success"})
#         else:
#             return JsonResponse(form.errors.get_json_data())
class BaseTeacherLoginView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_if_teacher))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class AssignedSections(BaseTeacherLoginView):
    def get(self, request):
        sections = CourseSection.objects.filter(teacher__user__username = str(request.user))
        from rest_framework.request import Request
        from initial.serializers import CourseSectionSerializer
        serial_sections = CourseSectionSerializer(sections, many=True,  context = {'request': Request(request)}).data

        if sections is None or serial_sections is None:
            return JsonResponse({'message':'Teacher has no assigned courses.','condition':True, 'sections':serial_sections}, status=200)
        else:
            return JsonResponse({'message':'Teacher has assigned courses.','condition':True, 'sections':serial_sections}, status=200)  



class StartSectionAttendance(BaseTeacherLoginView):
    def post(self, request):
        req_scsddc = request.POST['scsddc']
        slot = request.POST['slot']
        section = request.POST['section']
        if(slot is None or req_scsddc is None or section is None):
            return JsonResponse({'message':'Invalud Form Inputs','condition':False, }, status=200)
        print(request.POST)
        sec_att = SectionAttendance(scsddc = req_scsddc, attendance_slot = slot, section=section)
        sec_att.save()
        from rest_framework.request import Request
        from initial.serializers import SectionAttendanceSerializer
        data = SectionAttendanceSerializer(sec_att , context = {'request': Request(request)}).data
        
        if sec_att is None :
            return JsonResponse({'message':'Teacher has no assigned courses or Invalid scsddc.','condition':True, 'qr_json':data}, status=200)
        else:
            return JsonResponse({'message':'Attendance QR.','condition':True, 'qr_json':data}, status=200)          


@receiver(attendance_of_day_for_student)
def generate_attendance_for_student(**kwargs):
    pass
    # if kwargs['option'] == 'create':
    #     print('Received Signal For Creation Attendance of Day for student')
    #     SCSDDC_temp = str(kwargs['scsddc'])
    #     section = kwargs['coursesection']
    #     for student in section.students.all():
    #         new_sheet = StudentAttendance(scsddc = SCSDDC_temp)
    #         new_sheet.save()
        


    #     new_sheet.save()
    #     csection = CourseSection.objects.get(scsddc = SCSDDC_temp)
    #     csection.mark_sheet.add(new_sheet)
    #     print('Marksheet create')
    #     print(csection.mark_sheet.all())
    #     csection.save()
    #     return 'Success'
    # else:
    #     print('Received Signal For Deletion Attendance of Day for student')
    #     SCSDDC_temp = str(kwargs['course_section'])
        
    #     new_sheet = MarkSheet.objects.get(student = kwargs['student'], scsddc = SCSDDC_temp)
    #     csection = CourseSection.objects.get(scsddc = SCSDDC_temp)
    #     csection.mark_sheet.remove(new_sheet)
    #     new_sheet.delete()
    #     csection.save()
    #     return 'Success'


class Home_json(View):
        
    def get(self, request):
        print(dir(request))
        data_dict = model_to_dict(Teacher.objects.filter(user__username = request.user).first())
        user_data = model_to_dict(request.user)
        user_data.pop('groups',None)
        user_data.pop('password', None)
        print(data_dict)
        print(user_data)
        dat = {'status':'success',**data_dict,**user_data}
        
        return JsonResponse(dat)
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
class TeacherLoginView(View):

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
            dict_user.pop('groups',None)
            dict_user.pop('password', None)
            return JsonResponse({'status':'success','message' : 'User Logged In', **dict_user})
        else:
            return JsonResponse({'status':"Invalid Username of Password."}, status = 403)
        
        return HttpResponseRedirect('/home')

class TeacherLogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'status':'success','message' : 'User Logged Out'})



class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

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
