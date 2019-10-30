

from django.core.management.base import BaseCommand, CommandError
from ...root_commands import *
# from student_portal.models import Student
# from teacher_portal.models import Teacher

class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('operations', nargs='+', type=str)

        parser.add_argument(
            '--superuser',
            action='store_true',
            help = 'Create Super User'
        )
        parser.add_argument(
            '--deletesuperuser',
            action='store_true',
            help = 'Delete all Super User'
        )
        parser.add_argument(
            '--group',
            action='store_true',
            help = 'Create Groups'
        )
        parser.add_argument(
            '--deletegroup',
            action='store_true',
            help = 'Delete All Groups'
        )
        parser.add_argument(
            '--adduseringroup',
            action='store_true',
            help = 'Add users in Groups'
        )
        parser.add_argument(
            '--university',
            action='store_true',
            help = 'Add University'
        )
        parser.add_argument(
            '--semesterCore',
            action='store_true',
            help = 'Add Core semesters'
        )
        parser.add_argument(
            '--student',
            action='store_true',
            help = 'Add Students'
        )
        parser.add_argument(
            '--dropstudent',
            action='store_true',
            help = 'Drop all Students'
        )
    
    def handle(self, **options):

        if options['superuser']:
            #1 Add super users
            create_super_users()

        if options['deletesuperuser']:
            delete_super_users()

        if options['group']:
            #2 Create Groups
            create_groups()

        if options['deletegroup']:
            delete_groups()

        if options['adduseringroup']:
            add_users_in_group()
        
        if options['university']:
            add_university()
        
        if options['semesterCore']:
            add_semesterCore()
        
        if options['student']:
            insert_students()
        if options['dropstudent']:
            drop_all_students()

        # for operation in options['operations']:
        #     if operation == 'superuser':
        #     #1 Add super users
        #         self.create_super_users()
        #2 Add groups
        # print("I do Something")
        # print("Dropping All Students")
        # print("No. Of Students left : ", self.drop_all_students())
        # self.insert_students()
        #self.insert_degrees()
        #self.insert_students()
        #self.insert_course_loads()
        # self.insert_courses_csv()
    