from django.core.management.base import BaseCommand, CommandError
from initial.models import Student,User
import json
import os
from pprint import pprint

class Command(BaseCommand):
    def handle(self, **options):
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
            for d in data['Sheet1']:
                city_short = d['uid'][2]
            
                batch_short = d['uid'][0:2]
                roll = d['uid'][4:7]
                
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
        