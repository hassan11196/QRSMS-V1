from django.core.management.base import BaseCommand, CommandError
from initial.models import Student,User

class Command(BaseCommand):
    def handle(self, **options):
        # u = User(first_name = "saya",last_name = "dapra",email= "wohra@hotmail.com",password = 'redragon')
        # u.save()
        # print(u)
        # print("In test script")
        # s = Student.create("maya","khan", "maassa@hotmail.com",'redragon')
        u = User.objects.get(id=6)
        s = Student(user=u,uid=u.username,arn=1700006,batch=2017)
        print(s)
        print(u)
        s.save()
        