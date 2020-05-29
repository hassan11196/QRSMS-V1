from .models import Teacher
from .forms import TeacherForm
from initial.serializers import StudentInfoSectionModelSerializerGetAttendance, SectionAttendanceSerializer
from initial.models import CourseSection, SectionAttendance
import json
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from django.forms.models import model_to_dict


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.dispatch import receiver
from student_portal.models import Student
from initial.models import CourseSection, SectionAttendance, Course, StudentAttendance, SectionMarks, StudentMarks
from .serializers import (TeacherSerializer)
from .signals import attendance_of_day_for_student, marks_for_student
from django.db.utils import IntegrityError

from actor.serializers import LoginSerializer, UserSerializer
from initial.models import split_scsddc, Semester, MarkSheet


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


class BaseTeacherLoginView(APIView):
    @swagger_auto_schema()
    @csrf_exempt
    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_if_teacher))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TeacherAttendanceView(BaseTeacherLoginView):
    parser_classes = [JSONParser, MultiPartParser]

    @csrf_exempt
    @swagger_auto_schema()
    def post(self, request):
        try:
            query = request.data
            print('Request From : ' + str(request.user))
        except json.JSONDecodeError as err:

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

            # section_object = CourseSection.objects.get(
            #     section_name="E", course_code="CS309", semester_code="FALL2019_BS(CS)_ComputerSciences_MainCampus_Karachi", teacher__user__username=str('Abdul.Rehman'))
            print(section_object)

        except CourseSection.DoesNotExist as err:
            return JsonResponse({'status': 'Failure', 'message': 'Invalid Values', 'conditon': False, 'error': str(err)})

        students = StudentInfoSectionModelSerializerGetAttendance(
            section_object.student_info, many=True, context={'request': (request)}).data
        # print(students)

        scsddc = section + '_' + course_code + '_' + sddc
        try:
            attendance_list = SectionAttendance.objects.filter(scsddc=scsddc)
        except SectionAttendance.DoesNotExist as err:
            return JsonResponse({'status': 'Failure', 'message': 'Invalid Values', 'conditon': False, 'error': str(err)})
        class_attendance = SectionAttendanceSerializer(
            attendance_list, many=True, context={'request': (request)}).data
        print('Atteddance for this section : ' + str(len(attendance_list)))
        print('Students in this Section : ' + str(len(students)))
        # print(class_attendance)

        attendance_data = {
            'campus_name': city,
            'semester': semester_code,
            'course_code': course_code,
            'student_cnt': len(students),
            'attendance_cnt': len(attendance_list),
            'student_sheets': students,
            'class_sheet': class_attendance

        }

        return JsonResponse({'status': 'success', 'attendance_data': attendance_data})


class TeacherMarksView(BaseTeacherLoginView):
    def post(self, request):
        marks_type = request.POST['marks_type']
        scsddc = request.POST['scsddc']
        if marks_type == None or marks_type == "" or scsddc == None or scsddc == "" or scsddc=="null":
            return JsonResponse({"Failure": "Parameters Are Not Valid"}, safe=False,status=403)
        student_marks = StudentMarks.objects.filter(
            marks_type=marks_type, scsddc=scsddc).values()
        class_marks = SectionMarks.objects.filter(
            marks_type=marks_type, scsddc=scsddc).values()
        data = {
            "studentMarks": list(student_marks),
            "MarksInfo": list(class_marks)

        }
        return JsonResponse(data, safe=False)
import json
def update_marks(request):
    scsddc = request.POST['scsddc']
    marks_type = request.POST['marks_type']
    marks_data = json.loads(request.POST['marks_data'])
    if marks_type == None or marks_type == "" or scsddc == None or scsddc == "" or marks_data==None or marks_data =="":
        return JsonResponse({"Failed": "Invalid Input Parameters"}, status=403)
    else:
        try:
            for i in range(len(marks_data)):
                student_marks = StudentMarks.objects.get(marks_type=marks_type, scsddc=scsddc,pk = marks_data[i]['id'])
                old_weightage = student_marks.obtained_weightage
                student_marks.obtained_marks = marks_data[i]['obtained_marks']
                student_marks.obtained_weightage = marks_data[i]['obtained_weightage']
                student_marks.save()
                mark_sheet = MarkSheet.objects.get(student = Student.objects.get(uid=marks_data[i]['student_id']),scsddc = scsddc)
                mark_sheet.obtained_marks-= int(old_weightage)
                mark_sheet.obtained_marks += int(marks_data[i]['obtained_weightage'])
                mark_sheet.save()
                print(old_weightage)
                print(marks_data[i]['obtained_weightage'])
                print(mark_sheet.obtained_marks)
            student_marks = StudentMarks.objects.filter(marks_type=marks_type, scsddc=scsddc).values()
            class_marks = SectionMarks.objects.filter(marks_type=marks_type, scsddc=scsddc).values()
            data = {
                "Status":"Success",
                "studentMarks": list(student_marks),
                "MarksInfo": list(class_marks)

            }
            return JsonResponse(data,safe=False)
        except:
            data = {
                "Status":"Failed",
                "studentMarks": list(student_marks),
                "MarksInfo": list(class_marks)

            }




class AssignedSections(BaseTeacherLoginView):
    def get(self, request):
        sections = CourseSection.objects.filter(
            teacher__user__username=str(request.user)).all()

        from rest_framework.request import Request
        from initial.serializers import CourseSectionSerializer

        serial_sections = CourseSectionSerializer(sections, many=True,  context={
                                                  'request': request}).data
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
        course_code = request.POST['course_code']
        if(slot == '' or slot == 'null' or req_scsddc == '' or section == ''):
            return JsonResponse({'message': 'Invalud Form Inputs', 'condition': False, }, status=422)

        from initial.serializers import SectionAttendanceSerializer
        print(request.POST)

        current_semester = Semester.objects.filter(
            current_semester=True).latest()

        req_scsddc = f'{request.POST["section"]}_{request.POST["course_code"]}_{current_semester.semester_code}'

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
                sec_att2, context={'request': request}).data

            return JsonResponse({'message': 'Attendance Already Open For This Class.', 'condition': True, 'qr_json': data}, status=200)

        data = SectionAttendanceSerializer(
            sec_att, context={'request': request}).data

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

        if(marks_type is None or req_scsddc is None or section is None or req_scsddc is "null" ):
            return JsonResponse({'message': 'Invalid Form Inputs', 'condition': False, }, status=200)

        from rest_framework.request import Request
        from initial.serializers import SectionMarksSerializer
        print(request.POST)

        try:
            sec_marks = SectionMarks(scsddc=req_scsddc, marks_type=marks_type,
                                     section=section, total_marks=total_marks, weightage=weightage)
            sec_marks.save()
            g = marks_for_student.send(
                AddSectionMarks, scsddc=req_scsddc, coursesection=section, sectionmarks=sec_marks, option='create')
            print(g)
        except IntegrityError as e:

            # data = SectionMarksSerializer(
            #     sec_att2, context={'request': request}).data

            return JsonResponse({'message': 'Marks Already Added For This Class.'}, status=200)

        if sec_marks is None:
            return JsonResponse({'message': 'Teacher has no assigned courses or Invalid scsddc.', 'condition': True, 'qr_json': data}, status=200)
        else:
            return JsonResponse({'message': 'Marks Open For This Section.', 'condition': True}, status=200)


@receiver(marks_for_student)
def generate_marks_for_student(**kwargs):
    semester = Semester.objects.get(current_semester=True)
    year = semester.semester_year
    season = semester.semester_season
    if kwargs['option'] == 'create':
        print('Received Signal For Creation Marks of Day for student')
        SCSDDC_temp = str(kwargs['scsddc'])
        section_marks = kwargs['sectionmarks']
        section = kwargs['coursesection']
        scsddc_dict = split_scsddc(SCSDDC_temp)
        csection = CourseSection.objects.get(
            section_name=scsddc_dict['section'], course_code=scsddc_dict['course_code'], semester_code="_".join(SCSDDC_temp.split('_')[2:]))

        for student_info in csection.student_info.all():
            new_a = StudentMarks(marks_type=section_marks.marks_type, total_marks=section_marks.total_marks, scsddc=section_marks.scsddc,
                                 student=student_info.student, weightage=section_marks.weightage, section=section_marks.section)
            new_a.save()
            info = csection.student_info.get(student=student_info.student)
            
            info.mark_sheet.Marks.add(new_a)
            if info.mark_sheet.grand_total_marks==None:
                info.mark_sheet.grand_total_marks =0.0 
            info.mark_sheet.grand_total_marks += int(section_marks.weightage)
            info.mark_sheet.year = year
            info.mark_sheet.semester_season = season
            info.mark_sheet.save()

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


class TeacherLoginView(APIView):

    def get(self, request, *args, **kwargs):
        return HttpResponse("PLease Login" + str(kwargs))

    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: UserSerializer(many=True)})
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        if username == "" or password == "":
            return Response(data="Empty Usename or Password Field.", status=400)

        user = authenticate(request, username=username, password=password)

        print(user)

        if user is not None and user.is_teacher:
            login(request, user)
            dict_user = model_to_dict(user)
            dict_user.pop('groups', None)
            dict_user.pop('password', None)
            return Response({'status': 'success', 'message': 'User Logged In', **dict_user})
        else:
            if not user.is_teacher:
                return Response({'status': "User not a Teacher. Contact Admin"}, status=401)
            return Response({'status': "Invalid Username of Password."}, status=403)

        return HttpResponseRedirect('/home')


class TeacherLogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'User Logged Out'})


@receiver(attendance_of_day_for_student)
def generate_attendance_for_student(**kwargs):
    if kwargs['option'] == 'create':
        print('Received Signal For Creation Attendance of Day for student')
        SCSDDC_temp = str(kwargs['scsddc'])
        section_attendance = kwargs['sectionattendance']
        section = kwargs['coursesection']
        scsddc_dict = split_scsddc(SCSDDC_temp)
        csection = CourseSection.objects.get(
            section_name=scsddc_dict['section'], course_code=scsddc_dict['course_code'], semester_code="_".join(SCSDDC_temp.split('_')[2:]))

        for student_info in csection.student_info.all():
            new_a = StudentAttendance(attendance_type='M', state='A', scsddc=section_attendance.scsddc, student=student_info.student, class_date=section_attendance.class_date,
                                      attendance_slot=section_attendance.attendance_slot, duration_hour=section_attendance.duration_hour, section=section_attendance.section)
            new_a.save()
            info = csection.student_info.get(student=student_info.student)
            info.attendance_sheet.attendance.add(new_a)
            print(new_a)
        return 'Success'


def marks_info(request):
    scsddc = request.POST['scsddc']
    print(scsddc)
    if scsddc == None or scsddc == "" or scsddc=="null":
        return JsonResponse({"Failed": "Invalid Input Parameters"},status=403)
    print(scsddc)
    marks = SectionMarks.objects.filter(scsddc=scsddc).values()
    return JsonResponse(list(marks), safe=False)


def generate_grades(request):
    
    grades = {
        1:"A+",
        2:"A",
        3:"A-",
        4:"B+",
        5:"B",
        6:"B-",
        7:"C+",
        8:"C",
        9:"C-",
        10:"D+",
        11:"D",
        12:"D-",
        13:"F"

    }
    gpas = {
        1:"4.00",
        2:"4.00",
        3:"3.67",
        4:"3.33",
        5:"3.00",
        6:"2.67",
        7:"2.33",
        8:"2.00",
        9:"1.67",
        10:"1.33",
        11:"1.00",
        12:"F"

    }

    #grading_type = request.POST['Type']
    scheme = 0
    scsddc = request.POST['scsddc']
    if scsddc==None or scsddc == "" or scsddc == "null":
        return JsonResponse({"Error":"Invalid scsddc"},status=403)
    csection = CourseSection.objects.get(scsddc = scsddc)
    for student_info in csection.student_info.all():
        info = csection.student_info.get(student=student_info.student)
        weight = info.mark_sheet.obtained_marks
        if(weight >90):
            info.mark_sheet.grade = grades[1-scheme]
            info.mark_sheet.gpa = gpas[1-scheme]
        elif(weight<90 and weight>85):
            info.mark_sheet.grade = grades[2-scheme]
            info.mark_sheet.gpa = gpas[2-scheme]
        elif(weight<86 and weight>81):
            info.mark_sheet.grade = grades[3-scheme]
            info.mark_sheet.gpa = gpas[3-scheme]
        elif(weight<82 and weight>77):
            info.mark_sheet.grade = grades[4-scheme]
            info.mark_sheet.gpa = gpas[4-scheme]
        elif(weight<78 and weight>73):
            info.mark_sheet.grade = grades[5-scheme]
            info.mark_sheet.gpa = gpas[5-scheme]
        elif(weight<74 and weight>69):
            info.mark_sheet.grade = grades[6-scheme]
            info.mark_sheet.gpa = gpas[6-scheme]
        elif(weight<70 and weight>65):
            info.mark_sheet.grade = grades[7-scheme]
            info.mark_sheet.gpa = gpas[7-scheme]
        elif(weight<66 and weight>61):
            info.mark_sheet.grade = grades[8-scheme]
            info.mark_sheet.gpa = gpas[8-scheme]
        elif(weight<62 and weight>57):
            info.mark_sheet.grade = grades[9-scheme]
            info.mark_sheet.gpa = gpas[9-scheme]
        elif(weight<58 and weight>53):
            info.mark_sheet.grade = grades[10-scheme]
            info.mark_sheet.gpa = gpas[10-scheme]
        elif(weight<54 and weight>49):
            info.mark_sheet.grade = grades[11-scheme]
            info.mark_sheet.gpa = gpas[11-scheme]
        else:
            info.mark_sheet.grade = grades[12-scheme]
            info.mark_sheet.gpa = gpas[12-scheme]
        info.mark_sheet.finalized = True
        current_Sem = Semester.objects.get(current_semester=True)
        transcript = Transcript.objects.get(student = student_info.student,Semester=current_sem)
        sum = 0
        count = 0
        last_course_being_final = True
        for sheet in transcript.course_result:
            if last_course_being_final and sheet.finalized == False:
                last_course_being_final = False
            sum+=sheet.gpa
            count+=1            

        sgpa = sum/count
        transcript.sgpa = sgpa
        if weight >49:
            transcript.credit_hours_earned+=info.mark_sheet.course.credit_hour
        transcript.credit_hours_attempted+=info.mark_sheet.course.credit_hour
        transcript.save()
        all_transcript = Transcript.objects.get(student = student_info.student)
        sum = 0
        count = 0
        for tr in all_transcript:
            if last_course_being_finalized:
                tr.last = False
            sum+=tr.sgpa
            count+=1
        transcript.cgpa = sum/count
        if last_course_being_finalized:
            transcript.last = True
    return JsonResponse("Success")