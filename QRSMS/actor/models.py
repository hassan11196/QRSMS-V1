

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, ValidationError
from django.urls import reverse

from institution.constants import UNIVERISTY_ID_REGEX

# from initial.models import Semester, BATCH_YEAR_REGEX, STUDENT_YEAR_CHOICE, SEMSESTER_CHOICES, ACADEMIC_YEAR
# Create your models here.

BATCH_YEAR_REGEX = RegexValidator(
    "[0-9]{4}", message="Invalid Batch Year")

CNIC_REGEX = RegexValidator(
    "[0-9]{5}-[0-9]{7}-[0-9]{1}", message="Invalid CNIC")

SEMSESTER_CHOICES = (
        (1, "FALL"),
        (2, "SPRING"),
        (3, "SUMMER")
    )
STUDENT_YEAR_CHOICE = (
        (1, "FRESHMEN"),
        (2, "SOPHOMORE"),
        (3, "JUNIOR"),
        (4 ,"SENIOR"),
        (5,"VETERAN")
    )

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

    permanent_address = models.TextField(null=True)
    permanent_home_phone = models.PositiveIntegerField(null=True)
    permanent_postal_code = models.PositiveIntegerField(null=True)
    permanent_city = models.TextField(max_length=100,null=True)
    permanent_country = models.TextField(max_length=100,null=True)
    current_address = models.TextField(null=True)
    current_home_phone = models.PositiveIntegerField(null=True)
    current_postal_code = models.PositiveIntegerField(null=True)
    current_city = models.TextField(max_length=100,null=True)
    current_country = models.TextField(max_length=100,null=True)

    
    DOB = models.DateField(verbose_name='Date of Birth',null=True)
    nationality = models.CharField(verbose_name='Nationality', max_length=100,null=True)
    mobile_contact = models.PositiveIntegerField(verbose_name='Mobile Contact',null=True)
    emergency_contact = models.PositiveIntegerField(verbose_name='Emergency Contact',null=True)


    def __str__(self):
        return self.username
    



