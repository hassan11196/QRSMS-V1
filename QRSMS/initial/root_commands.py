import json
import os
from pprint import pprint
import datetime
from django.db import connection
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from actor.models import User
from initial.models import (ACADEMIC_YEAR, STUDENT_YEAR_CHOICE, Course,
                            RegularCoreCourseLoad, Semester)
from institution.models import Degree, University, Campus, Department
from student_portal.models import Student
from teacher_portal.models import Teacher
from institution.constants import DEFAULT_PASSWORD

CURRENT_SEMESTER = 'Fall'  # , 0 , (1,'Fall')

def random_func():
    add_teachers()


def setup_university():
    add_students('Dumps/students2.json',5)
    add_university()
    add_campuses()
    add_departments()
    add_degrees()

def add_students_in_department():
    dep = Department.objects.get(department_id = 1)
    for stud in Student.objects.all():
        dep.department_students.add(stud)
    dep.save()
def add_teachers_in_department():
    pass

def add_users_in_group():
    for user in User.objects.all():
        if user.is_maintainer or user.is_staff:
            user.groups.add(Group.objects.get(name='maintainer_group'))
            print('Added ' + str(user) + ' in ' + 'maintainer_group')
        if user.is_student:
            user.groups.add(Group.objects.get(name='student_group'))
            print('Added ' + str(user) + ' in ' + 'student_group')
        if user.is_teacher:
            user.groups.add(Group.objects.get(name='teacher_group'))
            print('Added ' + str(user) + ' in ' + 'teacher_group')
        if user.is_faculty:
            user.groups.add(Group.objects.get(name='faculty_group'))
            print('Added ' + str(user) + ' in ' + 'faculty_group')

def add_teachers():
    
    teachers =["Zulfiqar.Ali.Memon","Anum.Qureshi","Tania.Irum","Ammara.Yaseen","Mohammad.Faheem","Abdul.Rehman","Javeria.Farooq","Syeda.Rubab.Jaffar","M.Nadeem","Hamza.Ahmed","Atif.Tahir","Zeshan.Khan","M.Waqas","Hasina.Khatoon","Hassan.Jamil.Syed"]

    for teacher in teachers:
        t = Teacher.create(nu_email= teacher+'nu.edu.pk',username = teacher,password = DEFAULT_PASSWORD)
        print(t)

def delete_groups():
    status = Group.objects.all().delete()
    print('All Groups Deleted')


def create_groups():
    GROUPS = ['student_group', 'teacher_group',
              'faculty_group', 'maintainer_group']
    PERMISSIONS = ['add', 'change', 'delete', 'view']
    MODELS = ['student', 'teacher', 'faculty']

    for group, model in zip(GROUPS, MODELS):
        new_group, created_group = Group.objects.get_or_create(name=group)
        print(str(new_group) + str(created_group))
        for permission in PERMISSIONS:
            # perm_name = model+'_portal' + "|" + model + "|" +
            #perm_name = permission + '_' + model
            perm_name = 'Can {} {}'.format(permission, model)
            print('creating ' + perm_name)
            try:

                model_add_perm = Permission.objects.get(name=perm_name)
            except PermissionError as e:
                print('Error ' + e)
                continue
            new_group.permissions.add(model_add_perm)

    # maintainer group
    new_group, created_group = Group.objects.get_or_create(name=GROUPS[3])
    print(str(new_group) + str(created_group))
    for model in MODELS:
        for permission in PERMISSIONS:
            # perm_name = model+'_portal' + "|" + model + "|" +
            #perm_name = permission + '_' + model
            perm_name = 'Can {} {}'.format(permission, model)
            print('creating ' + perm_name)
            try:

                model_add_perm = Permission.objects.get(name=perm_name)
            except PermissionError as e:
                print('Error ' + e)
                continue
            new_group.permissions.add(model_add_perm)


def delete_super_users():
    User.objects.get(is_staff=True).delete()
    print('Super User Deleted')


def drop_all_students():
    User.objects.filter(is_student=True).delete()
    print('All Students Deleted')
    # create_super_users()
    # User.objects.get(username!='admin11196').delete()

    return True


def create_super_users():
    nu = User(username='admin11196',
              email='hassan11196@hotmail.com', is_staff=True)
    nu.set_password('adminhassanqrsms')
    nu.is_superuser = True
    nu.is_maintainer = True
    nu.save()
    nu = User(username='admin3650',
              email='ahsan11196@hotmail.com', is_staff=True)
    nu.set_password('adminahsanqrsms')
    nu.is_superuser = True
    nu.is_maintainer = True
    nu.save()
    return nu


def insert_core_course_loads():
    cloads = ["CL101 CS101 MT101 SS111 SS101 SL101 EE182",
              "SS113 CS103 EE227 EL227 MT115 CL103 SS122",
              "EE213 MT104 CS211 EL213 CS201",
              "SS103 CL205 CS301 MT206 CS205",
              "CL309 CS302 CS203 EE204 CS309 CL203"
              ]
    deg = Degree.objects.get(degree_short='BS(CS)')
    for sem, cload in enumerate(cloads):
        clist = cload.split(" ")
        r1 = RegularCoreCourseLoad(semester_season=int(
            ((sem) % 2)+1), student_year=int((sem/2) + 1), credit_hour_limit=19, degree=deg)
        print(r1)
        r1.save()
        for c in clist:
            print(Course.objects.get(course_code=c))
            r1.courses.add(Course.objects.get(course_code=c))


def insert_degrees():
    # Insert Degree
    Degree.objects.all().delete()

    nd = Degree(
        minimium_years_education=12,
        completion_year=16,
        duration=4,
        education_level="Bachelors",
        degree_name="Computer Science",
        degree_short="BS(CS)",
    )
    nd.save()
    nd = Degree(
        minimium_years_education=12,
        completion_year=16,
        duration=4,
        education_level="Bachelors",
        degree_name="Electrical Engineering",
        degree_short="BS(EE)",
    )
    nd.save()
    nd = Degree(
        minimium_years_education=12,
        completion_year=16,
        duration=4,
        education_level="Bachelors",
        degree_name="Business Administration",
        degree_short="BBA",
    )
    nd.save()


def add_students(file_name = 'Dumps\Students.json', count = 20):
    # u = User(first_name = "saya",last_name = "dapra",email= "wohra@hotmail.com",password = 'redragon')
    # u.save()
    # print(u)
    # print("In test script")
    # s = Student.create("maya","khan", "maassa@hotmail.com",'redragon')
    # u = User.objects.get(id=6)
    # s = Student(user=u,uid=u.username,arn=1700006,batch=2017)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(BASE_DIR)
    # print(os.path.join(BASE_DIR,'..','..','Dumps/Student.json'))

    drop_all_students()

    with open(os.path.join(BASE_DIR, file_name), 'r') as json_file:

        students_object_list = []
        uni_domain = "nu.edu.pk"
        DEFAULT_PASSWORD = 'hassan'
        data = json.load(json_file)
        # pprint(data)
        for d in data[:count]:
            # pprint(d)
            city_short = d['uid'][2]

            batch_short = d['uid'][0:2]
            batch_year = int("20"+batch_short)
            roll = d['uid'][4:8]

            temp_name = d['name'].split(" ")
            d['first_name'] = temp_name[0]
            if(len(temp_name) > 1):
                d['last_name'] = " ".join(temp_name[1:])
            else:
                d['last_name'] = ""

            d['is_student'] = True
            d['batch'] = "20" + d['uid'][0:2]
            d['arn'] = str(d['uid'][0:2]) + str(d['arn'])

            if d['Department'] == 'BBA':
                d['degree_name'] = "Bachelors of Business Administration"
                d['degree_short'] = 'BBA'
                d['department_name'] = 'Management Sciences'

            elif d['Department'] == 'BS(CS)':
                d['degree_name'] = "Bachelors of Computer Science"
                d['degree_short'] = 'BS(CS)'
                d['department_name'] = 'Computer Science'

            elif d['Department'] == 'BS(SE)':
                d['degree_name'] = "Bachelors of Software Engineering"
                d['degree_short'] = 'BS(SE)'
                d['department_name'] = 'Computer Science'

            elif d['Department'] == 'BS(EE)':
                d['degree_name'] = "Bachelors of Electrical Engineering"
                d['degree_short'] = 'BS(EE)'
                d['department_name'] = 'Electrical Engineering'

            # print(batch_year)
            # print(ACADEMIC_YEAR - batch_year)
            d['warning_count'] = 0
            d['student_year'] = (
                ACADEMIC_YEAR - batch_year) if (ACADEMIC_YEAR - batch_year) <= 4 else 4
            # print(d['student_year'])
            d['uni_mail'] = city_short + batch_short + roll + '@' + uni_domain
            d['attending_semester'] = True
            d['current_semester'] = 1  # Hardcode to Fall Semester
            created_user = User.create(first_name=d.get('first_name'),
                                last_name=d.get('last_name'),
                                email=d.get('registration_mail'),
                                username=d.get('uid'),
                                gender=d.get('gender'),
                                is_student=True,
                                CNIC=d.get('CNIC'),
                                permanent_address=d.get('address'),
                                permanent_home_phone=d.get('home_phone'),
                                permanent_postal_code=d.get('postal_code'),
                                permanent_city=d.get('city'),
                                permanent_country=d.get('country'),
                                current_address=d.get('address'),
                                current_home_phone=d.get('home_phone'),
                                current_postal_code=d.get('postal_code'),
                                current_city=d.get('city'),
                                current_country=d.get('country'),
                                nationality='Pakistani',
                                DOB=d.get('DOB'),
                                mobile_contact=d.get('mobile_contact'),
                                emergency_contact=d.get('emergency_contact'),
                                password = DEFAULT_PASSWORD
                                )
            # created_user.set_password(DEFAULT_PASSWORD)
            # created_user.save()
            # pprint(d)
            created_student = Student(user=created_user,
                                      uid=d.get('uid'),
                                      arn=d.get('arn'),
                                      batch=d.get('batch'),
                                      degree_name_enrolled=d.get(
                                          'degree_name'),
                                      degree_short_enrolled=d.get(
                                          'degree_short'),
                                      department_name_enrolled=d.get(
                                          'department_name'),
                                      uni_mail=d.get('uni_mail'),
                                      student_year=d.get('student_year'),
                                      attending_semester=d.get(
                                          'attending_semester'),
                                      warning_count=d.get('warning_count'),
                                      admission_section = d.get('Section')
                                      # current_semester = Semester.objects.get(semester_season = d.get('current_semester'))
                                      )
            
            # pprint(d)
            created_student.save()
            students_object_list.append(created_student)

    return students_object_list


def add_university(arg_uni_id=101101, arg_name='National University of Computing and Emerging Sciences'):
    University.objects.all().delete()
    u = University(
        uni_id=arg_uni_id,
        name=arg_name
    )
    u.save()
    return u


def add_campuses(arg_uni_id=101101,arg_campus_id=1, arg_campus_address='St-4 Sector 17-D On National Highway Karachi , Pakistan',
                 arg_campus_name='MAIN CAMPUS', arg_campus_city='Karachi', arg_contact_no=9221341005416,
                 arg_contact_email='info@nu.edu.pk',
                 arg_campus_country='Pakistan'):
    campus = Campus(
        uni_name=University.objects.get(uni_id=arg_uni_id),
        campus_id = arg_campus_id,
        campus_address=arg_campus_address,
        campus_name=arg_campus_name,
        campus_city=arg_campus_city,
        contact_no=arg_contact_no,
        contact_email=arg_contact_email,
        campus_country=arg_campus_country
    )

    campus.save()

    return campus


def add_departments(arg_campus_id = 1, arg_department_id = 1, arg_department_name = 'Computer Sciences'):
    department = Department(
        campus_id = arg_campus_id,
        department_id = arg_department_id,
        department_name = arg_department_name
    )
    department.save()
    return department

def add_degrees(arg_offering_department = 1, arg_education_level = 'Bachelors', arg_degree_name = 'Computer Science', arg_degree_short = 'BS(CS)'):
    degree = Degree(
        offering_department = Department.objects.get(department_id = arg_offering_department),
        education_level = arg_education_level,
        degree_name= arg_degree_name,
        degree_short = arg_degree_short,
        minimium_years_education=12,
        completion_year=16,
        duration=4,
    )
    degree.save()
    nd = Degree(
        offering_department = Department.objects.get(department_id =arg_offering_department),
        minimium_years_education=12,
        completion_year=16,
        duration=4,
        education_level="Bachelors",
        degree_name="Electrical Engineering",
        degree_short="BS(EE)",
    )
    nd.save()
    # nd = Degree(
    #     offering_department = Department.objects.get(department_id =arg_offering_department),
    #     minimium_years_education=12,
    #     completion_year=16,
    #     duration=4,
    #     education_level="Bachelors",
    #     degree_name="Business Administration",
    #     degree_short="BBA",
    # )
    # nd.save()
    return degree

def add_semesterCore():
    Semester.objects.all().delete()
    
    # temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    s = Semester(
        semester_code='FALL2019',
        semester_season=1,
        semester_year=2019,
        start_date=datetime.strptime('19-08-2019', "%d-%m-%Y").date(),
        end_date=datetime.strptime('19-12-2019', "%d-%m-%Y").date(),
    )
    s.save()
    return s


def add_courses():
    Course.objects.all().delete()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    course_dict = [
        "course_code",
        "course_name",
        "credit_hour",
        "type"
    ]
    courses = []

    with open(os.path.join(BASE_DIR, 'Dumps\course.csv'), 'r') as csv_file:
        next(csv_file)  # Skip first row
        for d in csv_file:
            temp = d.split(',')
            print(temp)
            temp[3] = temp[3].strip()
            courses.append(temp)

            if temp[3] == 'Core':
                ctype = 1
            elif temp[3] == 'Elective':
                ctype = 2
            else:
                ctype = 3

            nc = Course(
                course_code=temp[0], course_name=temp[1], credit_hour=temp[2], course_type=ctype)
            nc.save()
    return courses
