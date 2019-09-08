from django.db import models

# Create your models here.
class course(models.Model):
    course_name = models.CharField(max_length=50,name="course_name")
    course_code = models.CharField(max_length=20,primary_key = True, name="course_code")
    course_short = models.CharField(max_length=50)