from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,ValidationError
from institution.models import University, Campus, Degree, UNIVERISTY_ID_REGEX



CNIC_REGEX = RegexValidator(
    "[0-9]{5}-[0-9]{7}-[0-9]{1}", message="Invalid CNIC")
BATCH_YEAR_REGEX = RegexValidator(
    "[0-9]{4}",message="Invalid Batch Year")



class User(AbstractUser):
    username = models.CharField("username", max_length=50,unique=True,null=False)
    GENDERS = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('U', 'UNDEFINED'),
        ('O', 'OTHER')
    ]
    gender = models.CharField(
        "Gender", name="gender", max_length=50, choices=GENDERS)

    is_teacher = models.BooleanField(
        default=False, help_text='True if the User is a Teacher.')
    is_student = models.BooleanField(
        default=False, help_text='True if the User is a Student.')
    is_faculty = models.BooleanField(
        default=False, help_text='True if the User is a Faculty Member.')
    is_maintainer = models.BooleanField(
        default=False, help_text='True if the User is a Mainatiner or Project Developer.')
    CNIC = models.CharField(max_length=15, validators=[
                            CNIC_REGEX], name="CNIC")

# Create your models here.


class Course(models.Model):
    course_name = models.CharField(max_length=50, name="course_name")
    course_code = models.CharField(
        max_length=20, primary_key=True, name="course_code")
    course_short = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name


# class Student(models.Model):
#     student_id = models.CharField(max_length=8,primary_key=True, validators = [RegexValidator("^[A-Z][0-9]{2}-[0-9]{4}$", message = "Invalid Student ID")], name="student_id_n")

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    department = models.CharField(max_length=10)
    nu_email = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Faculty Supervisors"





class Student(models.Model):
    @classmethod
    def create(cls, first_name,last_name,email,password, *args, **kwargs):
        print(first_name + last_name+ email+ password)
        user_created = User(first_name = first_name, last_name = last_name, password = password, email=email, is_student=True)
        user_created.save()
        last_student = Student.objects.all().order_by('arn').last()
        
        if not last_student:
            print("last studnet is empty")
            last_arn_number =  ((17%100)*1000000)+1
        else:
            last_arn_number = last_student.arn + 1
            
        
        student_created = cls(user=user_created,arn=last_arn_number)
        
        print("Returning created student")
        print(student_created )

        return student_created

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    batch = models.PositiveSmallIntegerField("batch year", validators=[BATCH_YEAR_REGEX])
    arn = models.PositiveIntegerField(
        "Admission Registration Number", name='arn',primary_key=True)
    
    uid = models.CharField("Student ID", default="00K-0000", name="uid",
                           max_length=8, validators=[UNIVERISTY_ID_REGEX], help_text="University Student Roll Number")

    def __str__(self):
        return self.user.username

   

      

class Semester(models.Model):
    offered_courses = models.ManyToManyField(
        Course, related_name="semester_offered")
    SEMSESTER_CHOICES = (
        (1, "FALL"),
        (2, "SPRING"),
        (3, "SUMMER")
    )
    semester_time = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    semester_year = models.DateField(name="Semester Year")
    start_date = models.DateField(name="Semester Start Date")
    end_date = models.DateField(name="Semester End Date")
    teachers_available = models.ManyToManyField(
        Teacher, related_name="teachers_available")
    students_registered = models.ManyToManyField(
        Student, related_name="students_registered")
