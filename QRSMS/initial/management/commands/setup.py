

# from __future__ import print_function, unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands import flush
from ...root_commands import *
from pprint import pprint
from PyInquirer import prompt, print_json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('operations', nargs='+', type=str)
        pass

    def handle(self, **options):
        print('Welcome To QRSMS')

        answers = prompt([{
            'type': 'confirm',
            'name': 'new_project',
            'message': 'Do you want to start Fresh Project Configuration?',
        }])

        if answers['new_project']:
            print('1) Flushing old DB: ')
            flush()
            print('Super User Setup: ')

        else:
            print('Have a good day then. :)')
            # answers = prompt([{
            #     'type': 'confirm',
            #     'name': 'new_migrations',
            #     'message': 'Do you want to Clear migrations?',
            # }])

        # for operation in options['operations']:
        #     if operation == 'superuser':
        #     #1 Add super users
        #         self.create_super_users()
        # 2 Add groups
        # print("I do Something")
        # print("Dropping All Students")
        # print("No. Of Students left : ", self.drop_all_students())
        # self.insert_students()
        # self.insert_degrees()
        # self.insert_students()
        # self.insert_course_loads()
        # self.insert_courses_csv()
