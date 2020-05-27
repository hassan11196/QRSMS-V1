

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator, ValidationError
from django.urls import reverse
from institution.constants import UNIVERISTY_ID_REGEX
import datetime
# from initial.models import Semester, BATCH_YEAR_REGEX, STUDENT_YEAR_CHOICE, SEMSESTER_CHOICES, ACADEMIC_YEAR
# Create your models here.
from json import loads, dumps
from collections import OrderedDict


def ordered_to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


BATCH_YEAR_REGEX = RegexValidator(
    "[0-9]{4}", message="Invalid Batch Year")

CNIC_REGEX = RegexValidator(
    "[0-9]{5}-[0-9]{7}-[0-9]{1}", message="Invalid CNIC")

SEMSESTER_CHOICES = (
    (1, "SPRING"),
    (2, "FALL"),
    (3, "SUMMER")
)
STUDENT_YEAR_CHOICE = (
    (1, "FRESHMEN"),
    (2, "SOPHOMORE"),
    (3, "JUNIOR"),
    (4, "SENIOR"),
    (5, "VETERAN")
)
CURRENT_SEMESTER = 1  # FALL
CURRENT_SEMESTER_CODE = 'FALL2019_BS(CS)_ComputerSciences_MainCampus_Karachi'


class User(AbstractUser):
    username = models.CharField(
        "username", max_length=50, unique=True, null=False)
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

    is_employee = models.BooleanField(
        default=False, help_text='True if the User is a Employee of Institution')

    employee = models.OneToOneField(
        'actor.Employee', null=True, on_delete=models.CASCADE)

    CNIC = models.CharField(max_length=15, validators=[
                            CNIC_REGEX], name="CNIC")

    permanent_address = models.TextField(null=True)
    permanent_home_phone = models.PositiveIntegerField(null=True)
    permanent_postal_code = models.PositiveIntegerField(null=True)
    permanent_city = models.TextField(max_length=100, null=True)
    permanent_country = models.TextField(max_length=100, null=True)
    current_address = models.TextField(null=True)
    current_home_phone = models.PositiveIntegerField(null=True)
    current_postal_code = models.PositiveIntegerField(null=True)
    current_city = models.TextField(max_length=100, null=True)
    current_country = models.TextField(max_length=100, null=True)

    DOB = models.DateField(verbose_name='Date of Birth',
                           null=True, default=datetime.date.today)
    nationality = models.CharField(
        verbose_name='Nationality', max_length=100, null=True)
    mobile_contact = models.PositiveIntegerField(
        verbose_name='Mobile Contact', null=True)
    emergency_contact = models.PositiveIntegerField(
        verbose_name='Emergency Contact', null=True)

    educational_history = models.OneToOneField(
        "actor.EducationalHistory", verbose_name="Educational Histories", on_delete=models.CASCADE, null=True)

    def __str__(self):
        # if self.is_student:
        #     return self.first_name + " " + self.last_name
        return self.username

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, username, password, is_teacher=False, is_maintainer=False, is_student=False, is_employee=False, is_faculty=False, employee=None, *args, **kwargs):
        if is_faculty or is_teacher:
            is_employee = True
            if employee is None:
                e = Employee.create()
                employee = e
        user = cls(username=username, is_teacher=is_teacher, is_maintainer=is_maintainer, is_student=is_student,
                   is_employee=is_employee, is_faculty=is_faculty, employee=employee, *args, **kwargs)
        user.set_password('hassan')
        user.save()
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

        return user


class EducationalHistory(models.Model):
    pass


class EmployeeDesignation(models.Model):
    designation_id = models.IntegerField(primary_key=True)
    designation_name = models.CharField(max_length=256, null=True)

    @classmethod
    def create(cls, **kwargs):
        e = cls(**kwargs)
        e.save()
        return e

    @classmethod
    def create_or_get_teacher(cls):
        te, created = cls.objects.get_or_create(designation_name='Teacher')

        return te

    def __str__(self):
        return self.designation_name


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_designation = models.ManyToManyField('actor.EmployeeDesignation')
    hire_date = models.DateField(null=True, default=datetime.date.today)
    salary = models.PositiveIntegerField(null=True)

    @classmethod
    def create(cls, **kwargs):
        e = cls(**kwargs)
        e.save()
        ed = EmployeeDesignation.create_or_get_teacher()
        e.employee_designation.add(ed)

        return e

    def __str__(self):
        return "  ENo: " + str(self.employee_id) + ", Designations :" + ",".join([str(designations) for designations in self.employee_designation.all()])
