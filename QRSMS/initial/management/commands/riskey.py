from django.core.management.base import BaseCommand, CommandError
from initial.models import Student,User, Course, RegularCoreCourseLoad
from institution.models import Degree
import json
import os
from pprint import pprint
from django.db import connection

class Command(BaseCommand):
    def handle(self, **options):
        # print("I do Something")
        # print("Dropping All Students")
        # print("No. Of Students left : ", self.drop_all_students())
        # self.insert_students()
        #self.insert_degrees()
        # self.insert_students()
        # self.create_super_users()
        self.insert_course_loads()
        # self.insert_courses_csv()
       
    def drop_all_students(self):

        Student.objects.all().delete()
        self.create_super_users()
        # User.objects.get(username!='admin11196').delete()

        return User.objects.all()

    def create_super_users(self):
        User.objects.all().delete()
        nu = User(username = 'admin11196', email='hassan11196@hotmail.com', is_staff=True)    
        nu.set_password('adminhassanqrsms')
        nu.is_superuser = True
        nu.save()
        nu = User(username = 'admin3650', email='ahsan11196@hotmail.com', is_staff=True)    
        nu.set_password('adminahsanqrsms')
        nu.is_superuser = True
        nu.save()
        print(nu)

    def insert_course_loads(self):
        cloads = ["CL101 CS101 MT101 SS111 SS101 SL101 EE182",
        "SS113 CS103 EE227 EL227 MT115 CL103 SS122",
        "EE213 MT104 CS211 EL213 CS201",
        "SS103 CL205 CS301 MT206 CS205",
        "CL309 CS302 CS203 EE204 CS309 CL203"
        ]
        deg = Degree.objects.get(degree_short='BS(CS)')
        for sem,cload in enumerate(cloads):
            clist = cload.split(" ")
            r1 = RegularCoreCourseLoad(semester_season=int(((sem)%2)+1),student_year=int((sem/2) + 1),credit_hour_limit=19,degree=deg)
            print(r1)
            r1.save()
            for c in clist:
                print(Course.objects.get(course_code=c))
                r1.courses.add(Course.objects.get(course_code=c))
       
        

    def insert_degrees(self):
        # Insert Degree
        Degree.objects.all().delete()

        nd = Degree(
            minimium_years_education = 12,
            completion_year = 16,
            duration = 4,
            education_level = "Bachelors",
            degree_name = "Computer Science",
            degree_short = "BS(CS)",
        )
        nd.save()
        nd = Degree(
            minimium_years_education = 12,
            completion_year = 16,
            duration = 4,
            education_level = "Bachelors",
            degree_name = "Electrical Engineering",
            degree_short = "BS(EE)",
        )
        nd.save()
        nd = Degree(
            minimium_years_education = 12,
            completion_year = 16,
            duration = 4,
            education_level = "Bachelors",
            degree_name = "Business Administration",
            degree_short = "BBA",
        )
        nd.save()

    def insert_students(self):
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


        with open(os.path.join(BASE_DIR,'..','..','Dumps\Students.json'), 'r') as json_file:

            uni_domain = "nu.edu.pk"
            DEFAULT_PASSWORD = 'hassan'
            data = json.load(json_file)
            # pprint(data)
            for d in data:
                city_short = d['uid'][2]
            
                batch_short = d['uid'][0:2]
                roll = d['uid'][4:8]
                
                temp_name = d['name'].split(" ")
                d['first_name'] = temp_name[0]
                if(len(temp_name) > 1):
                    d['last_name'] = " ".join(temp_name[1:])
                else:
                    d['last_name'] = ""

                d['is_student'] = True
                d['batch'] = "20" + d['uid'][0:2]
                d['arn'] = d['uid'][0:2] + d['arn']

                
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

                
                d['uni_mail'] = city_short + batch_short+ roll + '@' + uni_domain

                created_user = User(first_name=d.get('first_name'),
                            last_name=d.get('last_name'),
                            email=d.get('registration_mail'),
                            username=d.get('uid'),
                            gender=d.get('gender'),
                            is_student=True,
                            CNIC=d.get('CNIC'),
                            permanent_address = d.get('address'),
                            permanent_home_phone = d.get('home_phone'),
                            permanent_postal_code = d.get('postal_code'),
                            permanent_city = d.get('city'),
                            permanent_country = d.get('country'),
                            current_address = d.get('address'),
                            current_home_phone = d.get('home_phone'),
                            current_postal_code = d.get('postal_code'),
                            current_city = d.get('city'),
                            current_country = d.get('country'),
                            nationality = 'Pakistani',
                            DOB = d.get('DOB'),
                            mobile_contact = d.get('mobile_contact'),
                            emergency_contact = d.get('emergency_contact')
                            )
                created_user.set_password(DEFAULT_PASSWORD)
                created_user.save()
                created_student = Student(user=created_user,
                                        uid=d.get('uid'),
                                        arn=d.get('arn'),
                                        batch=d.get('batch'),
                                        degree_name_enrolled = d.get('degree_name'), 
                                        degree_short_enrolled = d.get('degree_short'),
                                        department_name_enrolled = d.get('department_name'),
                                        uni_mail = d.get('uni_mail')
                                        )
                pprint(d)
                created_student.save()

            
            
        # print(s)
        # print(u)
        # s.save()
    def insert_courses_csv(self):
        Course.objects.all().delete()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        course_dict = [
            "course_code",
            "course_name",
            "credit_hour",
            "type"
        ]
        courses = []

        with open(os.path.join(BASE_DIR,'..','..','Dumps\course.csv'), 'r') as csv_file:
            next(csv_file) # Skip first row
            for d in csv_file:
                temp = d.split(',')
                print(temp)
                temp[3] =  temp[3].strip()
                courses.append(temp)
    
                if temp[3] == 'Core':
                    ctype = 1
                elif temp[3] == 'Elective':
                    ctype = 2
                else :
                    ctype = 3

                nc = Course(course_code = temp[0], course_name=temp[1], credit_hour=temp[2], course_type=ctype)
                nc.save()


        

    