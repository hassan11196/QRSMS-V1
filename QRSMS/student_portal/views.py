from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from drf_yasg.utils import swagger_auto_schema

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
from django.contrib.auth.decorators import user_passes_test
import io
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from initial.models import SectionAttendance, AttendanceSheet, StudentAttendance, Course
from actor.models import CURRENT_SEMESTER, CURRENT_SEMESTER_CODE, ordered_to_dict
from .serializers import StudentSerializer, StudentSerializerAllData
from rest_framework import viewsets, views, status, mixins
from .forms import StudentForm, StudentFormValidate
from .models import Student, FeeChallan
from initial.models import Semester
# Create your views here.


class UserNotLogged(View):
    def get(self, request):
        return JsonResponse({'message': 'Not Authenticated'}, status=401)


def check_if_student(user):
    return True if user.is_student else False


class BaseStudentLoginView(views.APIView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_if_student, login_url='/student/login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Home_json(BaseStudentLoginView):

    def get(self, request):
        print((request.user))
        stud_obj = Student.objects.filter(uid=str(request.user))
        print(stud_obj)
        user_obj = request.user

        dict_user = model_to_dict(user_obj)
        dict_user.pop('groups', None)
        dict_user.pop('password', None)

        student_data = StudentSerializer(stud_obj, many=True).data

        dat = {'status': 'success',
               'student_data': student_data, 'user_data': dict_user}

        return JsonResponse(dat)


class AttendanceView(BaseStudentLoginView):
    def get(self, request, course_code):
        from initial.models import AttendanceSheet, OfferedCourses
        print(dir(self))
        print(dir(request.user))
        s = Student.objects.get(uid=request.user)
        csddc = course_code + "_" + s.semester_code
        at = AttendanceSheet.objects.get(
            student__uid=request.user, scsddc__endswith=csddc)

        from initial.serializers import AttendanceSheetSerializer
        att_serialized = AttendanceSheetSerializer(at, many=True).data

        return JsonResponse({'message': 'Available Attendacne', 'condition': True, 'attendance': att_serialized}, status=200)


class PostAttendanceQR(BaseStudentLoginView):
    def post(self, request):
        print(request.POST['qr_code'])
        import json
        request_data = json.loads(request.POST['qr_code'])
        print(request_data)
        print(request.user)
        try:
            att_object = StudentAttendance.objects.get(student=Student.objects.get(uid=str(
                request.user)), scsddc=request_data['scsddc'], class_date=request_data['class_date'], attendance_slot=request_data['attendance_slot'], section=request_data['section'])
        except StudentAttendance.DoesNotExist as e:
            return JsonResponse({'message': 'Student is not enrolled in this Class', 'condition': False}, status=400)

        if att_object.state == 'P':
            return JsonResponse({'message': 'Attendance Already Marked', 'condition': True, }, status=200)
        att_object.state = 'P'
        att_object.save()
        from initial.serializers import StudentAttendanceSerializer
        from rest_framework.request import Request
        data = StudentAttendanceSerializer(
            att_object, context={'request': Request(request)}).data

        return JsonResponse({'message': 'Attendance Marked', 'condition': True, 'attendance': data}, status=200)


class TimeTableView(BaseStudentLoginView):
    def get(self, request):
        import requests
        uid = str(request.user)
        city = uid[2].lower()
        rnum = uid[4:]
        year = uid[0:2]
        url = 'https://timetablenotifier.com/api/fetch.php?email="' + \
            str(city+year+rnum) + '@nu.edu.pk"'
        print(url)
        r = requests.get(url)
        data = r.json()
        return JsonResponse(data)


class RegistrationCheck(BaseStudentLoginView):
    def get(self, request):
        print(request.user)
        from institution.models import Department, Degree
        try:
            s = Student.objects.get(uid=request.user)
            dep = Department.objects.get(
                department_name=s.department_name_enrolled)
            deg = Degree.objects.get(
                degree_short=s.degree_short_enrolled, offering_department=dep)

        except Degree.DoesNotExist as e:
            return JsonResponse({'message': 'Invalid Student. Degree Does not Exist', 'condition': True, 'error_raised': True, 'error': str(e)}, status=401)

        except Department.DoesNotExist as e:
            return JsonResponse({'message': 'Invalid Student. Department Does not Exist', 'condition': True, 'error_raised': True}, status=401)

        if dep is None or deg is None:
            return JsonResponse({'message': 'Invalid Student', 'condition': True}, status=401)

        if(deg.registrations_open == True):
            return JsonResponse({'message': 'Regisrations are Active', 'condition': True}, status=200)
        else:
            return JsonResponse({'message': 'Regisrations are NOT Active', 'condition': False}, status=200)


class RegistrationCourses(BaseStudentLoginView):
    @swagger_auto_schema()
    def get(self, request):
        from institution.models import Department, Degree
        try:
            s = Student.objects.get(uid=request.user)
            if s.warning_count > 0:
                return JsonResponse({'message': 'Student in Warning. Conatact Academic Office.', 'condition': False}, status=200)
            from initial.models import Semester, OfferedCourses
            # sem = Semester.objects.get(semester_code=CURRENT_SEMESTER_CODE)
            # rg_courses = sem.regular_course_load.get(semester_season=CURRENT_SEMESTER,student_year=s.student_year)
            # el_courses = sem.elective_course_load.get(semester_season=CURRENT_SEMESTER)

            s = OfferedCourses.objects.filter(student__uid=str(request.user))

            # from rest_framework.request import Request

            from initial.serializers import OfferedCoursesSerializer
            offered_courses_to_student = OfferedCoursesSerializer(
                s, many=True, context={'request': request}).data

            from pprint import pprint
            pprint(offered_courses_to_student)

        except Semester.DoesNotExist as e:
            return JsonResponse({'message': 'Invalid Semester. Contact Adminstration.', 'condition': False, 'error_raised': True}, status=401)

        except OfferedCourses.DoesNotExist as e:
            return JsonResponse({'message': 'Invalid Student. Department Does not Exist', 'condition': False, 'error_raised': True}, status=401)

        if offered_courses_to_student is None:
            return JsonResponse({'message': 'No Available Courses', 'condition': False}, status=401)

        return JsonResponse({'message': 'Available Courses', 'condition': True, 'regular_courses': offered_courses_to_student}, status=200)


class StudentSignupView(View):
    def post(self, request):
        form = StudentFormValidate(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return JsonResponse({'status': "Success", 'message': 'Student Sign Up Successful.'})
        else:
            return JsonResponse(form.errors.get_json_data())


class StudentLoginView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("PLease Login" + str(kwargs))

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if username is "" or password is "":
            return HttpResponse(content="Empty Usename or Password Field.", status=400)

        user = authenticate(request, username=username, password=password)
        if user.is_student == False:
            return JsonResponse({'status': "User not a Student."}, status=401)

        if user is not None:
            login(request, user)
            # dict_user = model_to_dict(user)
            # dict_user.pop('groups',None)
            # dict_user.pop('password', None)
            return JsonResponse({'status': 'success', 'message': 'User Logged In'})
        else:
            return JsonResponse({'status': "Invalid Username of Password."}, status=403)

        return HttpResponseRedirect('/home')


class StudentLogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'User Logged Out'})


# def generate_challan(request):
#     student = Student.objects.get(user = request.user)
#     semester = Semester.objects.get(semester_code= request.POST['semester'])
#     csr = request.POST['course'].split(',')
#     challan = FeeChallan.object.create(student=student,semester=semester)
#     fee_per_Cr = semester.fee_per_CR
#     fee = 0
#     for c in csr:
#         challan.coursea.add(Course.object.get(course_code=c))
#         fee+=fee_per_Cr
#     challan.Tution_fee = fee
#     challan.total_fee = fee
#     challan.save()

def update_challan(request):
    admission_fee = request.POST['admission_fee']
    student = Student.objects.get(user=request.user)
    semester = Semester.objects.get(semester_code=request.POST['semester'])
    challan, created = FeeChallan.objects.get_or_create(
        student=student, semester=semester)
    option = request.POST['action']
    code = request.POST['code']
    course = Course.objects.get(course_code=code)
    course_fee = semester.fee_per_CR
    if option == 'drop':
        challan.course.remove(course)
        challan.total_fee = challan.total_fee-course_fee
    else:
        challan.course.add(course)
        challan.total_fee = challan.total_fee+course_fee
        if(admission_fee != ''):
            challan.total_fee += admission_fee
    challan.save()


def get_challan(request):
    student = Student.objects.get(user=request.user)
    semester = Semester.objects.get(semester_code=request.POST['code'])
    challan = FeeChallan.objects.get(student=student, semester=semester)
    challan_obj = {
        "due_date": challan.due_date,
        "name": request.user.first_name+request.user.last_name,
        "roll_no": student.uid,
        "challan_no": "123456678",
        "discipline": student.degree_short_enrolled+'('+student.department_name_enrolled+')',
        "semester": semester.semester_season+" "+semester.semester_year,
        "admission_fee": challan.admission_fee,
        "tution_fee": challan.tution_fee,
        "fine": challan.Fine,
        "other": challan.other_charges+challan.coActivity_charges,
        "arrears": challan.Arrear,
        "withholding": challan.withholding_tax,
        "total_amount": challan.total_fee,
        "fine_per_day": challan.total_fee*0.001,


    }
    return JsonResponse(list(challan_obj, safe=False))

