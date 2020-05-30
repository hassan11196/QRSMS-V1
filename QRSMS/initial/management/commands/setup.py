

# from __future__ import print_function, unicode_literals
from colorama import Fore, Back, Style, init
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from pprint import pprint

import os
from ...root_commands import create_super_users, create_groups, setup_university, create_groups
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('operations', nargs='+', type=str)
        parser.add_argument(
            '--default',
            action='store_true',
            help='Use Pre-defined Defaults. useful for seeing how the project works without customization.'
        )

    def handle(self, **options):
        init(autoreset=True)
        use_default_settings = options['default']
        interactive = not use_default_settings
        print(Fore.BLUE + 'QRSMS Project Setup')
        if not use_default_settings:
            answer = input('Do you want to start Fresh Project Configuration? (y/n)')


        if use_default_settings or answer == '' or answer.lower() == 'y' or answer.lower() == 'yes':
            print(Fore.GREEN + '1) Flushing old DB: ')
            call_command('flush', interactive=interactive)
            call_command('sqlflush')
            call_command('reset_db', interactive=interactive)
            print(Fore.BLUE + 'DB Flushed Successfully. ')

            print(Fore.GREEN + '2) Making Migrations: ')
            call_command('makemigrations', interactive=interactive)
            print(Fore.BLUE + 'Migrations made Successfully. ')

            print(Fore.GREEN + '3) Migrate Schema to DB: ')
            call_command('migrate', interactive=interactive)
            print(Fore.BLUE + 'Schema Migrations made Successfully. ')

            print(Fore.GREEN + '4) Super User Setup: ')
            if use_default_settings:
                create_groups()
                create_super_users()
                print(Fore.BLUE + 'Super User Created Successfully. ')

                print(Fore.GREEN +
                      '6) Default University Setup: ')
                setup_university()
                print(Fore.BLUE + 'University setup complete. ')

            else:
                call_command('createsuperuser')
                print(Fore.BLUE + 'Super User Created Successfully. ')

                print(
                    Fore.RED + 'You now have to set the institutions model as per your own requirements using the admin panel. ')
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
