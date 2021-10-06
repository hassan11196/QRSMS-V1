import json

from colorama import Back, Fore, Style, init
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count
from django.db.utils import IntegrityError
from django.dispatch import receiver
import statistics
from django.forms.models import model_to_dict
# Create your views here.
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from actor.serializers import LoginSerializer, UserSerializer
from helpers.decorators import user_passes_test
from initial.models import (Course, CourseSection, MarkSheet,
                            SectionAttendance, SectionMarks, Semester,
                            StudentAttendance, StudentMarks, Transcript,
                            split_scsddc)
from initial.serializers import (
    SectionAttendanceSerializer,
    StudentInfoSectionModelSerializerGetAttendance,CourseSectionSerializer,SectionMarksSerializer)
from student_portal.models import Student

from .forms import TeacherForm
from .models import Teacher
from .serializers import TeacherSerializer
from .signals import attendance_of_day_for_student, marks_for_student


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
    not_user_response = {'message': 'Login Required',
                         'condtion': False, 'status': 'failure'}
    not_teacher_response = {'message': 'User Logged in is Not a Teacher',
                            'condtion': False, 'status': 'failure'}

    @ method_decorator(user_passes_test(lambda u: u.is_authenticated, on_failure_json_response=JsonResponse(not_user_response, status=401)))
    @ method_decorator(user_passes_test(check_if_teacher, on_failure_json_response=JsonResponse(not_teacher_response, status=401)))
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
            return JsonResponse({'status': 'Failure', 'message': 'Malformed Query', 'conditon': False, 'missing key': str(err)}, 400)

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
            'class_sheet': class_attendance,
            'section': query['section']
        }

        return JsonResponse({'status': 'success', 'attendance_data': attendance_data})


class TeacherMarksView(BaseTeacherLoginView):
    def post(self, request):
        marks_type = request.POST['marks_type']
        scsddc = request.POST['scsddc']
        if marks_type == None or marks_type == "" or scsddc == None or scsddc == "" or scsddc == "null":
            return JsonResponse({"Failure": "Parameters Are Not Valid"}, safe=False, status=403)
        student_marks = StudentMarks.objects.filter(
            marks_type=marks_type, scsddc=scsddc)
        class_marks = SectionMarks.objects.filter(
            marks_type=marks_type, scsddc=scsddc).values()
        marks_data = []

        for student_marks in student_marks:
            obj = {
                "id": student_marks.id,
                "marks_type": student_marks.marks_type,
                "total_marks": student_marks.total_marks,
                "weightage": student_marks.weightage,
                "obtained_marks": student_marks.obtained_marks,
                "obtained_weightage": student_marks.obtained_weightage,
                "student_id": student_marks.student.uid,
                "student_name": student_marks.student.user.first_name+" "+student_marks.student.user.last_name,

            }
            marks_data.append(obj)
        data = {
            "studentMarks": marks_data,
            "MarksInfo": list(class_marks)

        }
        return JsonResponse(data, safe=False)

def change_marks_dist(request):
    scsddc = request.POST['scsddc']
    marks_type = request.POST['marks_type']
    new_marks_type = request.POST['new_type']
    old_weightage = request.POST['old_weightage']
    new_weightage = request.POST['new_weightage']
    old_marks  = request.POST['old_marks']
    new_marks = request.POST['new_marks']
    if scsddc == "null" or scsddc == "" or marks_type == "null" or marks_type == "" or new_marks_type == "null" or new_marks_type == "" or old_weightage == "null" or new_weightage == "null" or old_marks == "null" or new_marks == "null" or old_weightage == "" or new_weightage == "" or old_marks == "" or new_marks == "":
        return JsonResponse({"Status":"Failed","Message":" Invalid Input"},status=403)
    else:
        check = MarkSheet.objects.filter(
             scsddc=scsddc)
        if check[0].finalized:
            return JsonResponse({"Status":"Failed","Message":"Unable To Update Marks. Transcript Has been Generated"},status=403)
        try:
            section_marks = SectionMarks.objects.get(scsddc=scsddc,marks_type= marks_type)
            if section_marks.max_marks>float(new_marks):
                return JsonResponse({"Status":"Failed","Message":"Total Marks Are Less Than Max Marks Of Class"},status=200)
        except:
            return JsonResponse({"Status":"Failed","Message":"Marks Does Not Exist"},status=404)
        section_marks.total_marks = float(new_marks)
        section_marks.weightage = float(new_weightage)
        section_marks.marks_type = new_marks_type

        all_marks = []
        all_weightage = []
        student_marks = StudentMarks.objects.filter(
            marks_type=marks_type, scsddc=scsddc)
        for marks in student_marks:
            marksheet = MarkSheet.objects.get(scsddc=scsddc,student = marks.student)
            marks.marks_type = new_marks_type
            marks.total_marks = new_marks
            old_weight = marks.obtained_weightage
            old_total = marks.weightage
            marks.weightage = new_weightage
            marks.obtained_weightage = marks.obtained_marks/float(new_marks)*float(new_weightage)
            all_weightage.append(marks.obtained_marks/float(new_marks)*float(new_weightage))
            marksheet.grand_total_marks-=float(old_total)
            marksheet.grand_total_marks+=float(new_weightage)
            marksheet.obtained_marks-=old_weight
            marksheet.obtained_marks+=marks.obtained_marks/float(new_marks)*float(new_weightage)
            marks.save()
            marksheet.save()
        if len(all_marks) > 1:
            section_marks.weightage_mean = statistics.mean(all_weightage)
            section_marks.weightage_standard_deviation = statistics.stdev(
                all_weightage)

        else:

            section_marks.weightage_mean = all_weightage[0]
            section_marks.weightage_standard_deviation = 0

        section_marks.save()
        return JsonResponse({"Status":"Success","Message":"Evaluation Updated Successfully"})
        ######################################


def update_marks(request):
    scsddc = request.POST['scsddc']
    marks_type = request.POST['marks_type']
    marks_data = json.loads(request.POST['marks_data'])
    if marks_type == None or marks_type == "" or scsddc == None or scsddc == "" or marks_data == None or marks_data == "":
        return JsonResponse({"Failed": "Invalid Input Parameters"}, status=403)
    else:
        try:
            all_marks = []
            all_weightage = []
            for i in range(len(marks_data)):
                student_marks = StudentMarks.objects.get(
                    marks_type=marks_type, scsddc=scsddc, pk=marks_data[i]['id'])
                print(student_marks)
                old_weightage = student_marks.obtained_weightage
                student_marks.obtained_marks = marks_data[i]['obtained_marks']
                if float(student_marks.obtained_marks) > student_marks.total_marks:
                    return JsonResponse({"Failed": "Invalid Marks"}, status=403)
                student_marks.obtained_weightage = marks_data[i]['obtained_weightage']
                all_marks.append(float(marks_data[i]['obtained_marks']))
                all_weightage.append(
                    float(marks_data[i]['obtained_weightage']))
                student_marks.save()
                mark_sheet = MarkSheet.objects.get(student=Student.objects.get(
                    uid=marks_data[i]['student_id']), scsddc=scsddc)
                mark_sheet.obtained_marks -= int(old_weightage)
                mark_sheet.obtained_marks += int(
                    marks_data[i]['obtained_weightage'])
                mark_sheet.save()
                # print(old_weightage)
                # print(marks_data[i]['obtained_weightage'])
                # print(mark_sheet.obtained_marks)
            student_marks = StudentMarks.objects.filter(
                marks_type=marks_type, scsddc=scsddc).values()
            class_marks = SectionMarks.objects.get(
                marks_type=marks_type, scsddc=scsddc)
            if len(all_marks) > 1:
                class_marks.marks_mean = statistics.mean(all_marks)
                class_marks.marks_standard_deviation = statistics.stdev(
                    all_marks)
                class_marks.weightage_mean = statistics.mean(all_weightage)
                class_marks.weightage_standard_deviation = statistics.stdev(
                    all_weightage)
                class_marks.min_marks = min(all_marks)
                class_marks.max_marks = max(all_marks)
            else:
                class_marks.marks_mean = all_marks[0]
                class_marks.marks_standard_deviation = 0
                class_marks.weightage_mean = all_weightage[0]
                class_marks.weightage_standard_deviation = 0
                class_marks.min_marks = all_marks[0]
                class_marks.max_marks = all_marks[0]
            class_marks.save()
            class_marks = SectionMarks.objects.filter(
                marks_type=marks_type, scsddc=scsddc).values()
            print("Len")
            print(len(class_marks))
            data = {
                "Status": "Success",
                "studentMarks": list(student_marks),
                "MarksInfo": list(class_marks)

            }
            return JsonResponse(data, safe=False)
        except:
            data = {
                "Status": "Failed",
                "studentMarks": list(student_marks),
                "MarksInfo": list(class_marks)

            }
            return JsonResponse(data, safe=False)


class AssignedSections(BaseTeacherLoginView):
    def get(self, request):
        sections = CourseSection.objects.filter(
            teacher__user__username=str(request.user)).all()




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
        section = request.POST['scsddc'].split('_')[0]
        course_code = request.POST['course_code']
        if(slot == '' or slot == 'null' or req_scsddc == '' or section == ''):
            return JsonResponse({'message': 'Invalid Form Inputs', 'condition': False, }, status=422)


        print(request.POST)
        print(section)
        current_semester = Semester.objects.filter(
            current_semester=True).latest()

        req_scsddc = f'{section}_{request.POST["course_code"]}_{current_semester.semester_code}'
        print(req_scsddc)
        try:
            sec_att = SectionAttendance(
                scsddc=req_scsddc, attendance_slot=slot, section=section)
            sec_att.save()
            g = attendance_of_day_for_student.send(
                StartSectionAttendance, scsddc=req_scsddc, coursesection=section, sectionattendance=sec_att, option='create')
            print(g)
        except IntegrityError as e:
            print(Fore.RED + str(e))
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

        if(total_marks is None or total_marks=="" or total_marks=="null" or weightage is None or weightage == ""  or weightage == "null" or req_scsddc == "null" ):
            return JsonResponse({'message': 'Invalid Form Inputs', 'condition': False, }, status=200)
        if(marks_type is None or marks_type=="" or marks_type=="null" or req_scsddc is None or req_scsddc is ""  or section is None or req_scsddc == "null" ):
            return JsonResponse({'message': 'Invalid Form Inputs', 'condition': False, }, status=200)
        if(marks_type is None or section=="" or section=="null" or req_scsddc is None or req_scsddc == ""  or section is None or req_scsddc == "null" ):
            return JsonResponse({'message': 'Invalid Form Inputs', 'condition': False, }, status=200)




        print(request.POST)

        try:
            st1 = MarkSheet.objects.filter(scsddc=req_scsddc)
            print(len(st1))
            if len(st1)> 0 and st1[0].grand_total_marks + float(weightage)>100.0:
                return JsonResponse({"message": "Grand Total Can't be greater than 100"})
            if len(st1)> 0:
                print(st1[0].grand_total_marks+ float(weightage))
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
            return JsonResponse({'message': 'Teacher has no assigned courses or Invalid scsddc.', 'condition': True, }, status=200)
        else:
            return JsonResponse({'message': 'Marks Open For This Section.', 'condition': True}, status=200)


@receiver(marks_for_student)
def generate_marks_for_student(**kwargs):
    semester = Semester.objects.get(current_semester=True)
    year = semester.semester_year
    season = semester.semester_season
    if kwargs['option'] == 'create':
        print('Received Signal For Creation Marks for student')
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
            if info.mark_sheet.grand_total_marks == None:
                info.mark_sheet.grand_total_marks = 0.0
            info.mark_sheet.grand_total_marks += float(section_marks.weightage)
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
        if user is None:
            return Response({'status': "Invalid Username of Password."}, status=403)
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
        print(Fore.RED + scsddc_dict['section'])
        print(scsddc_dict['course_code'])
        print("_".join(SCSDDC_temp.split('_')[2:]))
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
    if scsddc == None or scsddc == "" or scsddc == "null":
        return JsonResponse({"Failed": "Invalid Input Parameters"}, status=403)
    print(scsddc)
    marks = SectionMarks.objects.filter(scsddc=scsddc).values()
    return JsonResponse(list(marks), safe=False)


def generate_grades(request):

    grades = {
        1: "A+",
        2: "A",
        3: "A-",
        4: "B+",
        5: "B",
        6: "B-",
        7: "C+",
        8: "C",
        9: "C-",
        10: "D+",
        11: "D",
        12: "F",


    }
    gpas = {
        1: 4.00,
        2: 4.00,
        3: 3.67,
        4: 3.33,
        5: 3.00,
        6: 2.67,
        7: 2.33,
        8: 2.00,
        9: 1.67,
        10: 1.33,
        11: 1.00,
        12: 0.00

    }

    #grading_type = request.POST['Type']
    scheme = 0
    scsddc = request.POST['scsddc']
    if scsddc == None or scsddc == "" or scsddc == "null":
        return JsonResponse({"Error": "Invalid scsddc"}, status=403)
    csection = CourseSection.objects.get(scsddc=scsddc)
    for student_info in csection.student_info.all():
        info = csection.student_info.get(student=student_info.student)
        weight = info.mark_sheet.obtained_marks
        old_gpa = info.mark_sheet.gpa
        if(weight >= 90):
            info.mark_sheet.grade = grades[1-scheme]
            info.mark_sheet.gpa = gpas[1-scheme]
        elif(weight < 90 and weight > 85):
            info.mark_sheet.grade = grades[2-scheme]
            info.mark_sheet.gpa = gpas[2-scheme]
        elif(weight < 86 and weight > 81):
            info.mark_sheet.grade = grades[3-scheme]
            info.mark_sheet.gpa = gpas[3-scheme]
        elif(weight < 82 and weight > 77):
            info.mark_sheet.grade = grades[4-scheme]
            info.mark_sheet.gpa = gpas[4-scheme]
        elif(weight < 78 and weight > 73):
            info.mark_sheet.grade = grades[5-scheme]
            info.mark_sheet.gpa = gpas[5-scheme]
        elif(weight < 74 and weight > 69):
            info.mark_sheet.grade = grades[6-scheme]
            info.mark_sheet.gpa = gpas[6-scheme]
        elif(weight < 70 and weight > 65):
            info.mark_sheet.grade = grades[7-scheme]
            info.mark_sheet.gpa = gpas[7-scheme]
        elif(weight < 66 and weight > 61):
            info.mark_sheet.grade = grades[8-scheme]
            info.mark_sheet.gpa = gpas[8-scheme]
        elif(weight < 62 and weight > 57):
            info.mark_sheet.grade = grades[9-scheme]
            info.mark_sheet.gpa = gpas[9-scheme]
        elif(weight < 58 and weight > 53):
            info.mark_sheet.grade = grades[10-scheme]
            info.mark_sheet.gpa = gpas[10-scheme]
        elif(weight < 54 and weight > 49):
            info.mark_sheet.grade = grades[11-scheme]
            info.mark_sheet.gpa = gpas[11-scheme]
        else:
            info.mark_sheet.grade = grades[12-scheme]
            info.mark_sheet.gpa = gpas[12-scheme]
        print(str(info.mark_sheet.grade)+" "+str(info.mark_sheet.gpa)+" "+str(weight))
        final_status = info.mark_sheet.finalized
        info.mark_sheet.finalized = True
        info.mark_sheet.save()
        current_sem = Semester.objects.get(current_semester=True)
        transcript = Transcript.objects.get(
            student=student_info.student, semester=current_sem)
        sum = 0
        count = 0
        last_course_being_final = True
        results = transcript.course_result.all()
        total_cr = 0
        for sheet in results:
            if last_course_being_final and sheet.finalized == False:
                last_course_being_final = False
            sum += sheet.gpa*sheet.course.credit_hour
            count += 1
            total_cr += sheet.course.credit_hour
        print(last_course_being_final)
        sgpa = sum/(total_cr)
        transcript.sgpa = sgpa
        if final_status is False:
            if weight > 49:
                transcript.credit_hours_earned += info.mark_sheet.course.credit_hour
            transcript.credit_hours_attempted += info.mark_sheet.course.credit_hour
        elif old_gpa == 0 and weight > 49 :
            transcript.credit_hours_earned += info.mark_sheet.course.credit_hour
        elif weight < 50:
            transcript.credit_hours_earned -= info.mark_sheet.course.credit_hour

        transcript.save()
        all_transcript = Transcript.objects.filter(
            student=student_info.student)
        print(all_transcript)
        sum = 0
        count = 0
        for tr in all_transcript:
            if last_course_being_final:
                tr.last = False
            sum += tr.sgpa
            count += 1

        transcript.cgpa = sum/count
        if last_course_being_final:
            transcript.last = True
        transcript.save()
    return JsonResponse("Success", safe=False)
