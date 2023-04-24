
import datetime
# from django.contrib.auth.decorators import user_passes_test
import io
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
# Create your views here.
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.views import APIView

from actor.models import (CURRENT_SEMESTER, CURRENT_SEMESTER_CODE,
                          ordered_to_dict)
from helpers.decorators import user_passes_test
from initial.models import (AttendanceSheet, Course, CourseStatus, MarkSheet,
                            OfferedCourses, SectionAttendance, SectionMarks,
                            Semester, StudentAttendance, StudentMarks,
                            Transcript)
from initial.serializers import (AttendanceSheetSerializer,
                                 OfferedCoursesSerializer, TranscriptSerilazer,StudentAttendanceSerializer)
from student_portal.serializers import StudentSerializerOnlyNameAndUid

from .forms import StudentForm, StudentFormValidate
from .models import FeeChallan, Student
from .serializers import StudentSerializer, StudentSerializerAllData

# Create your views here.


class UserNotLogged(View):
    def get(self, request):
        return JsonResponse({'message': 'Not Authenticated'}, status=401)


def check_if_student(user):
    return bool(user.is_student)


class BaseStudentLoginView(APIView):
    not_user_response = {'message': 'Login Required',
                         'condtion': False, 'status': 'failure'}
    not_student_response = {'message': 'User Logged in is Not a Student',
                            'condtion': False, 'status': 'failure'}

    @ method_decorator(user_passes_test(lambda u: u.is_authenticated, on_failure_json_response=JsonResponse(not_user_response, status=401)))
    @ method_decorator(user_passes_test(check_if_student, on_failure_json_response=JsonResponse(not_student_response, status=401)))
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
               'student_data': student_data, 'user_data': dict_user,  'data': student_data}

        return JsonResponse(dat)


class AttendanceView(BaseStudentLoginView):
    def get(self, request, course_code):

        print(dir(self))
        print(dir(request.user))
        s = Student.objects.get(uid=request.user)
        csddc = course_code + "_" + s.semester_code
        at = AttendanceSheet.objects.get(
            student__uid=request.user, scsddc__endswith=csddc)


        att_serialized = AttendanceSheetSerializer(at, many=True).data

        return JsonResponse({'message': 'Available Attendacne', 'condition': True, 'attendance': att_serialized}, status=200)


class PostAttendanceQR(BaseStudentLoginView):
    def post(self, request):
        print(request.POST['qr_code'])

        request_data = json.loads(request.POST['qr_code'])
        if isinstance(request_data, int):
            JsonResponse({'message': 'QR Not Scanned Properly. Please Try again',
                          'status': 'QR Scan Error', 'condition': False}, status=400)
        print(request_data)
        print(request.user)
        try:
            att_object = StudentAttendance.objects.get(student=Student.objects.get(uid=str(
                request.user)), scsddc=request_data['scsddc'], class_date=request_data['class_date'], attendance_slot=request_data['attendance_slot'], section=request_data['section'])
        except StudentAttendance.DoesNotExist as err:
            return JsonResponse({'message': 'Student is not enrolled in this Class', 'condition': False, 'error': err}, status=400)

        if att_object.state == 'P':
            return JsonResponse({'message': 'Attendance Already Marked', 'condition': True, }, status=200)
        att_object.state = 'P'
        att_object.save()


        data = StudentAttendanceSerializer(
            att_object, context={'request': request}).data

        return JsonResponse({'message': 'Attendance Marked', 'condition': True, 'attendance': data}, status=200)


class TimeTableView(BaseStudentLoginView):
    def get(self, request):
        # import requests
        # uid = str(request.user)
        # city = uid[2].lower()
        # rnum = uid[4:]
        # year = uid[0:2]
        # url = 'https://timetablenotifier.com/api/fetch.php?email="' + \
        #     str(city+year+rnum) + '@nu.edu.pk"'
        # print(url)
        # r = requests.get(url)
        # data = r.json()
        return JsonResponse({'data': [], 'message': 'TimeTable server is down', 'success': 0})


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
    @ swagger_auto_schema()
    def get(self, request):
        from institution.models import Department, Degree
        try:
            s = Student.objects.get(uid=request.user)
            if s.warning_count > 0:
                return JsonResponse({'message': 'Student in Warning. Conatact Academic Office.', 'condition': False}, status=200)

            # sem = Semester.objects.get(semester_code=CURRENT_SEMESTER_CODE)
            # rg_courses = sem.regular_course_load.get(semester_season=CURRENT_SEMESTER,student_year=s.student_year)
            # el_courses = sem.elective_course_load.get(semester_season=CURRENT_SEMESTER)
            current_semester = Semester.objects.filter(
                current_semester=True).latest()
            s = OfferedCourses.objects.filter(student__uid=str(
                request.user), semester_code=current_semester.semester_code)

            # from rest_framework.request import Request


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


class StudentLoginView(APIView):

    def get(self, request, *args, **kwargs):
        return HttpResponse("PLease Login" + str(kwargs))

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if username is "" or password is "":
            return JsonResponse({'message': "Empty Usename or Password Field.", 'status': 'failure'}, status=401)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'message': "Invalid Id Or Password", 'status': 'failure'}, status=403)

        if user.is_student == False:
            return JsonResponse({'message': 'User is Not a Student',
                                 'condtion': False, 'status': 'failure'}, status=401)

        if user is not None:
            login(request, user)
            dict_user = model_to_dict(user)
            dict_user.pop('groups', None)
            dict_user.pop('password', None)
            return JsonResponse({'status': 'success', 'message': 'User Logged In', **dict_user})
        else:
            return JsonResponse({'message': "Invalid Username of Password.", 'status': 'failure'}, status=403)

        return HttpResponseRedirect('/home')


class CustomOfferedCourseSerializer(ModelSerializer):
    # student = StudentSerializerOnlyNameAndUid()
    # courses = SerializerMethodField('registered_courses')

    # def registered_courses(self, offeredCourses):
    #     courses = ['gello']
    #     # for courseStatus in offeredCourses.courses_offered.all():
    #     #     print(CourseStatus)
    #     #     courses.append({
    #     #         'course_code': courseStatus.course.course_code,
    #     #         'course_name': courseStatus.course.course_name,
    #     #         'section': courseStatus.section
    #     #     })

    #     return courses

    class Meta:
        model = OfferedCourses
        fields = [
            # 'courses',
            'courses_offered'
        ]
        # fields = '__all__'


class StudentSectionView(BaseStudentLoginView):
    serializer_class = OfferedCoursesSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = None
    # queryset = OfferedCourses.objects.all()
    # filter_backends = [DjangoFilterBackend, OrderingFilter]

    # def get_queryset(self):
    #     current_semester = Semester.objects.filter(
    #         current_semester=True).latest()
    #     student = Student.objects.get(uid=self.request.user)
    #     courses = OfferedCourses.objects.filter(
    #         courses_offered__status='NR', student=student, semester_code=current_semester.semester_code)
    #     return courses

    # def filter_queryset(self, queryset):
    #     filter_backends = [DjangoFilterBackend]

    #     for backend in list(filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, view=self)
    #     return queryset

    @ swagger_auto_schema()
    def get(self, request, *args, **kwargs):

        current_semester = Semester.objects.filter(
            current_semester=True).latest()
        student = Student.objects.get(uid=self.request.user)
        courses = OfferedCourses.objects.get(
            student=student, semester_code=current_semester.semester_code)
        # courses_offered__status='NR', student=student, semester_code=current_semester.semester_code)
        processed_courses = []
        for courseStatus in courses.courses_offered.all():
            if courseStatus.status == "R":
                processed_courses.append({
                    'course_code': courseStatus.course.course_code,
                    'course_name': courseStatus.course.course_name,
                    'section': courseStatus.section,
                    'registration_status': courseStatus.status

                })

        # serialized_courses = OfferedCoursesSerializer(
        #     courses, many=True, context={'request': request}).data
        #  student=student, semester_code=current_semester.semester_code)
        # print(courses)
        # return Response(courses, status=200)
        return Response(processed_courses)


class StudentAttendanceView(BaseStudentLoginView):

    def get(self, request, *args, **kwargs):
        print(kwargs['section'])
        print(kwargs['course_code'])
        current_semester = Semester.objects.filter(
            current_semester=True).latest()
        student = Student.objects.get(uid=self.request.user)
        print(
            f'{kwargs["section"]}_{kwargs["course_code"]}_{current_semester.semester_code}')
        try:

            attendance_sheet = AttendanceSheet.objects.filter(
                student=student, scsddc=f'{kwargs["section"]}_{kwargs["course_code"]}_{current_semester.semester_code}'
            )
        except AttendanceSheet.DoesNotExist as e:
            return Response({'message': 'Error, Invalid Attendance Sheet Requested. Please contact admin.', 'error': str(e)}, status=400)

        print(type(attendance_sheet))
        sheet_serialized = AttendanceSheetSerializer(
            attendance_sheet, many=True, context={'request': request}).data
        return Response(sheet_serialized, status=200)


class StudentLogoutView(View):

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'success', 'message': 'User Logged Out', 'condtion': True})
        else:
            return JsonResponse({'status': 'success', 'message': 'No User Logged in', 'condtion': True})

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'success', 'message': 'User Logged Out', 'condtion': True})
        else:
            return JsonResponse({'status': 'success', 'message': 'No User Logged in', 'condtion': True})

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

    ts = int(datetime.datetime.now().timestamp())
    EndDate = datetime.date.today() + datetime.timedelta(days=30)
    admission_fee = request.POST['admission_fee']
    student = Student.objects.get(user=request.user)
    semester = Semester.objects.get(semester_code=request.POST['semester'])
    challan, created = FeeChallan.objects.get_or_create(
        student=student, semester=semester)
    if created == True:
        transcript = Transcript.objects.get_or_create(
            student=student, semester=Semester.objects.get(current_semester=True))[0]
        challan.coActivity_charges = semester.co_circular_fee
        challan.due_date = EndDate
        challan.challan_no = ts

    option = request.POST['action']
    code = request.POST['code']
    print(code)
    course = Course.objects.filter(course_name=code).first()
    credit_hour = course.credit_hour
    course_fee = semester.fee_per_CR
    if option == 'drop':
        challan.courses.remove(course)
        challan.tution_fee = challan.tution_fee-course_fee*credit_hour
        challan.total_fee = challan.total_fee-course_fee*credit_hour
    else:
        challan.courses.add(course)
        challan.tution_fee = challan.tution_fee+course_fee*credit_hour
        challan.total_fee = challan.total_fee+course_fee*credit_hour
        if(admission_fee != ''):
            challan.total_fee += int(admission_fee)
    challan.save()
    return JsonResponse("Success", safe=False)


def get_challan(request):
    student = Student.objects.get(user=request.user)

    code = request.POST['code']
    print(code)
    if len(code) > 1:
        semester = Semester.objects.get(semester_code=code)
        try:
            challan = FeeChallan.objects.get(
                student=student, semester=semester)
        except:
            return JsonResponse({"Error": "No Challan"}, safe=False, response=403)
    else:
        try:
            challan = FeeChallan.objects.filter(student=student).values()
            return JsonResponse(list(challan), safe=False)
        except:
            return JsonResponse({"Error": "No challan"}, safe=False, status=403)
    opt = semester.semester_season
    if(opt == 1):
        season = "Fall"
    elif opt == 2:
        season = "Spring"
    else:
        season = "Summer"
    challan_obj = {
        "due_date": challan.due_date,
        "name": request.user.first_name+request.user.last_name,
        "roll_no": student.uid,
        "discipline": student.degree_short_enrolled,
        "semester": season+" "+str(semester.semester_year),
        "admission_fee": challan.admission_fee,
        "tution_fee": challan.tution_fee,
        "fine": challan.Fine,
        "other": challan.other_charges+challan.coActivity_charges,
        "arrears": challan.Arrear,
        "withholding": challan.withholding_tax,
        "total_amount": challan.total_fee,
        "fine_per_day": int(challan.total_fee*0.001),
        "challan_no": challan.challan_no,
    }
    return JsonResponse(challan_obj, safe=False)


class Student_Transcript(View):

    def post(self, request):
        try:
            student = Student.objects.get(uid=request.POST['id'])
            transcript = Transcript.objects.filter(student=student)
            if len(transcript) > 1:
                json_transcript = TranscriptSerilazer(transcript, many=True)
                return JsonResponse(json_transcript.data, safe=False)

            else:
                transcript = Transcript.objects.get(student=student)
                json_transcript = TranscriptSerilazer(transcript)
                return JsonResponse([json_transcript.data], safe=False)
        except:
            return JsonResponse({"Error": "No Transcript"}, safe=False, status=420)


class StudentMarksView(View):
    def post(self, request):
        section = request.POST['section']
        code = request.POST['code']
        if section == None or section == "" or section == "null" or code == None or code == "" or code == "null":
            return JsonResponse({"Failed": "Invalid Input Parameters"}, status=403)
        else:
            student = Student.objects.get(user=request.user)
            semester = Semester.objects.get(current_semester=True)
            scsddc = section+"_"+code+"_"+semester.semester_code
            marks_info = SectionMarks.objects.filter(scsddc=scsddc)

            if(len(marks_info) > 0):
                marks_data = []
                for mark in marks_info:
                    marks = StudentMarks.objects.get(
                        student=student, scsddc=scsddc, marks_type=mark.marks_type)

                    obj = {
                        "marks_type": mark.marks_type,
                        "total_marks": marks.total_marks,
                        "weightage": marks.weightage,
                        "obtained_marks": marks.obtained_marks,
                        "obtained_weightage": marks.obtained_weightage,
                        "section": marks.section,
                        "marks_mean": mark.marks_mean,
                        "marks_std_dev": mark.marks_standard_deviation,
                        "weightage_mean": mark.weightage_mean,
                        "weightage_std_dev": mark.weightage_standard_deviation,
                        "min_marks": mark.min_marks,
                        "max_marks": mark.max_marks,
                    }
                    marks_data.append(obj)
                mark_sheet = MarkSheet.objects.get(
                    scsddc=scsddc, student=student)
                grand_total = {
                    "total_marks": mark_sheet.grand_total_marks,
                    "obtained_total": mark_sheet.obtained_marks,
                }
                return JsonResponse({"Status": "Success", "marks_info": marks_data, "total": [grand_total]}, safe=False, status=200)
            else:
                return JsonResponse({"Status": "Failed", "Message": "No Marks Available"}, status=200)


def get_scsddc(request):
    try:
        section = request.POST['section']
        code = request.POST['code']
        if code == 'null' or section == "null" or code == "" or section == "":
            return JsonResponse({"Failed": "Invalid Parameters"}, status=403)
    except:
        return JsonResponse({"Failed": "Invalid Parameters"}, status=403)
    semester = Semester.objects.get(
        current_semester=True)
    scsddc = section+"_"+code+"_"+semester.semester_code
    # mark_sheet = MarkSheet.objects.filter()
    return JsonResponse({"Status": "Success", "scsddc": scsddc})


def get_latest_transcript(request):
    student = Student.objects.get(user=request.user)
    transcript = Transcript.objects.filter(student=student, last=True).values()
    print(transcript)
    return JsonResponse(list(transcript), safe=False)
