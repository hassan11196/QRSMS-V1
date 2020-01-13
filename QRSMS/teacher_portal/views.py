import json
from django.db.models import Count
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
from rest_framework.request import Request
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.dispatch import receiver

from initial.models import CourseSection, SectionAttendance, Course, StudentAttendance,SectionMarks,StudentMarks
from .serializers import (TeacherSerializer)
from .signals import attendance_of_day_for_student,marks_for_student
from django.db.utils import IntegrityError

from initial.models import CourseSection, SectionAttendance
from initial.serializers import StudentInfoSectionModelSerializerGetAttendance, SectionAttendanceSerializer,SectionMarksSerializer
from .forms import TeacherForm
from .models import Teacher


def get_sddc(semester, degree, department, campus, city):
    return semester + "_" + degree + "_" + department + "_" + campus + "_" + city


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


class TeacherAttendanceView(BaseTeacherLoginView):
    def post(self, request):
        try:
            query = json.loads(request.body)
            print('Request From : ' + str(request.user))
        except json.JSONDecodeError as err:
            print(request.body)
            print(request)
            return JsonResponse({'status': 'Failure', 'message': 'Inavlid JSON Object', 'conditon': False, 'error': str(err)})
        try:
            city = query['city']  # "city":"Karachi"
            campus = query['campus']  # "campus":"MainCampus",
            # "department":"ComputerSciences",
            department = query['department']
            degree = query['degree']  # "degree":"BS(CS)",
            # "semester_code":"FALL2019",
            semester_code = query['semester_code']
            course_code = query['course_code']  # "course_code":"CS309",
            section = query['section']  # "section":"E"

        except KeyError as err:
            return JsonResponse({'status': 'Failure', 'message': 'Malformed Query', 'conditon': False, 'missing key': str(err)})

        
        sddc = get_sddc(semester_code, degree, department, campus, city)
        try:
            section_object = CourseSection.objects.get(
                section_name=section, course_code=course_code, semester_code=sddc, teacher__user__username=str(request.user))

        except CourseSection.DoesNotExist as err:
            return JsonResponse({'status': 'Failure', 'message': 'Invalid Values', 'conditon': False, 'error': str(err)})
        
        

        students =  StudentInfoSectionModelSerializerGetAttendance(section_object.student_info.all(), many=True, context={'request': Request(request)}).data
        # print(students)
        
        scsddc = section + '_' + course_code  +'_' + sddc
        try:
            attendance_list = SectionAttendance.objects.filter(scsddc = scsddc)
        except SectionAttendance.DoesNotExist as err:
            return JsonResponse({'status': 'Failure', 'message': 'Invalid Values', 'conditon': False, 'error': str(err)})
        
        class_attendance = SectionAttendanceSerializer(attendance_list, many=True, context={'request': Request(request)}).data
        print('Atteddance for this section : ' + str(len(attendance_list)))
        print('Students in this Section : ' + str(len(students)))
        # print(class_attendance)

        attendance_data = {
            'campus_name': city,
            'semester': semester_code,
            'course_code': course_code,
            'student_cnt': len(students),
            'attendance_cnt' : len(attendance_list),
            'student_sheets': students,
             'class_sheet': class_attendance

        }

        return JsonResponse({'status': 'success', 'attendance_data' : attendance_data})


class AssignedSections(BaseTeacherLoginView):
    def get(self, request):
        sections = CourseSection.objects.filter(
            teacher__user__username=str(request.user)).all()
        
        from rest_framework.request import Request
        from initial.serializers import CourseSectionSerializer
        serial_sections = CourseSectionSerializer(sections, many=True,  context={
                                                  'request': Request(request)}).data
        print(serial_sections)
        if sections is None or serial_sections is None:
            return JsonResponse({'message': 'Teacher has no assigned courses.', 'condition': True, 'sections': serial_sections}, status=200)
        else:
            return JsonResponse({'message': 'Teacher has assigned courses.', 'condition': True, 'sections': serial_sections}, status=200)


class StartSectionAttendance(BaseTeacherLoginView):
    def post(self, request):
        req_scsddc = request.POST['scsddc']
        slot = request.POST['slot']
        section = request.POST['section']
        if(slot is None or req_scsddc is None or section is None):
            return JsonResponse({'message': 'Invalud Form Inputs', 'condition': False, }, status=200)

        from rest_framework.request import Request
        from initial.serializers import SectionAttendanceSerializer
        print(request.POST)

        try:
            sec_att = SectionAttendance(
                scsddc=req_scsddc, attendance_slot=slot, section=section)
            sec_att.save()
            g = attendance_of_day_for_student.send(
                StartSectionAttendance, scsddc=req_scsddc, coursesection=section, sectionattendance=sec_att, option='create')
            print(g)
        except IntegrityError as e:
            sec_att2 = SectionAttendance.objects.get(
                scsddc=req_scsddc, attendance_slot=slot, section=section, class_date=sec_att.class_date)

            data = SectionAttendanceSerializer(
                sec_att2, context={'request': Request(request)}).data

            return JsonResponse({'message': 'Attendance Already Open For This Class.', 'condition': True, 'qr_json': data}, status=200)

        data = SectionAttendanceSerializer(
            sec_att, context={'request': Request(request)}).data

        if sec_att is None:
            return JsonResponse({'message': 'Teacher has no assigned courses or Invalid scsddc.', 'condition': True, 'qr_json': data}, status=200)
        else:
            return JsonResponse({'message': 'Attendance QR.', 'condition': True, 'qr_json': data}, status=200)


class AddSectionMarks(BaseTeacherLoginView):
    def post(self, request):
        req_scsddc = request.POST['scsddc']
        marks_type = request.POST['marks_type']
        total_marks = request.POST['total_marks']
        weightage = request.POST['weightage']
        section = request.POST['section']
        if(marks_type is None or req_scsddc is None or section is None):
            return JsonResponse({'message': 'Invalid Form Inputs', 'condition': False, }, status=200)

        from rest_framework.request import Request
        from initial.serializers import SectionMarksSerializer
        print(request.POST)

        try:
            sec_marks = SectionMarks(scsddc=req_scsddc, marks_type=marks_type, section=section, total_marks=total_marks, weightage=weightage)
            sec_marks.save()
            g = marks_for_student.send(
                AddSectionMarks, scsddc=req_scsddc, coursesection=section, sectionmarks=sec_marks, option='create')
            print(g)
        except IntegrityError as e:
            sec_att2 = SectionMarks.objects.get(
                scsddc=req_scsddc, marks_type=marks_type, section=section)

            data = SectionMarksSerializer(
                sec_att2, context={'request': Request(request)}).data

            return JsonResponse({'message': 'Maerks Already Added For This Class.', 'condition': True, 'qr_json': data}, status=200)

        data = SectionMarksSerializer(
            sec_marks, context={'request': Request(request)}).data

        if sec_marks is None:
            return JsonResponse({'message': 'Teacher has no assigned courses or Invalid scsddc.', 'condition': True, 'qr_json': data}, status=200)
        else:
            return JsonResponse({'message': 'Marks Open For This Section.', 'condition': True, 'qr_json': data}, status=200)


@receiver(marks_for_student)
def generate_marks_for_student(**kwargs):
    if kwargs['option'] == 'create':
        print('Received Signal For Creation Marks of Day for student')
        SCSDDC_temp = str(kwargs['scsddc'])
        section_marks = kwargs['sectionamarks']
        section = kwargs['coursesection']
        csection = CourseSection.objects.get(scsddc=SCSDDC_temp)
        for student_info in csection.student_info.all():
            new_a = StudentMarks(marks_type=section_marks.marks_type, total_marks=section_marks.total_marks, scsddc=section_marks.scsddc, student=student_info.student, weightage=section_marks.weightage
                                    , section=section_marks.section)
            new_a.save()
            info = csection.student_info.get(student=student_info.student)
            info.mark_sheet.Marks.add(new_a)
        return 'Success'


class Home_json(BaseTeacherLoginView):

    def get(self, request):
        print(dir(request))
        data_dict = model_to_dict(Teacher.objects.filter(
            user__username=request.user).first())
        user_data = model_to_dict(request.user)
        user_data.pop('groups', None)
        user_data.pop('password', None)
        print(data_dict)
        print(user_data)
        dat = {'status': 'success', **data_dict, **user_data}

        return JsonResponse(dat)


class TeacherLoginView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("PLease Login" + str(kwargs))

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if username is "" or password is "":
            return HttpResponse(content="Empty Usename or Password Field.", status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            dict_user = model_to_dict(user)
            dict_user.pop('groups', None)
            dict_user.pop('password', None)
            return JsonResponse({'status': 'success', 'message': 'User Logged In', **dict_user})
        else:
            return JsonResponse({'status': "Invalid Username of Password."}, status=403)

        return HttpResponseRedirect('/home')


class TeacherLogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'User Logged Out'})


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
