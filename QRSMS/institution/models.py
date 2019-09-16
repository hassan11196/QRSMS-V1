from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

UNIVERSITY_NAME = "FAST NUCES"
UNIVERSITY_FULL_NAME = "National University Of Computing And Emerging Sciences"
FOUNDATION_NAME = "Foundation for Advancement of Science And Technology"

CAMPUSES_CHOICES = (
    ('Karachi', 'K'),
    ('Lahore', 'L'),
    ('Faisalabad', 'F'),
    ('Islamabad', 'I'),
    ('Chiniot', 'C'),
    ('Peshawar', 'P')
)

CAMPUS_CHOICES_REGEX_STRING = "".join(map(lambda c: c[1], CAMPUSES_CHOICES))
UNIVERISTY_ID_REGEX = RegexValidator(
    "[0-9]{2}[" + CAMPUS_CHOICES_REGEX_STRING + "]-[0-9]{4}", message="INVALID ROLL NUMBER FORMAT")


class University(models.Model):
    class Meta:
        verbose_name_plural = "University"
    uni_id = models.AutoField(
        primary_key=True, name="uni_id", verbose_name="University Registration ID")
    name = models.CharField(
        max_length=255, help_text="Name of Univeristy")

    def __str__(self):
        return self.name
    

class Campus(models.Model):

    class Meta:
        verbose_name_plural = "Campuses"
    
    def __str__(self):
        return self.campus_name
    
    campus_id = models.AutoField(
        primary_key=True, name="campus_id", verbose_name="Campus ID")
    uni_name = models.ForeignKey("institution.University", on_delete=models.CASCADE,
                                 verbose_name="Universities Campus", help_text="A university can have many campuses")
    address = models.CharField(
        max_length=255, help_text="Address of Campus", name="Address")
    campus_name = models.CharField(
        max_length=255, help_text="Name of Campus of University")
    campus_city = models.CharField(
        max_length=255, help_text="City Name of Campus")


class Department(models.Model):
    campus = models.ForeignKey(
        Campus, on_delete=models.CASCADE, related_name="Campuses_Department")
    department_id = models.PositiveIntegerField(
        "Department ID", help_text="Department ID" ,primary_key = True)
    department_name = models.CharField("Department Name", max_length=255, help_text="Name of Department of Campus")

    def __str__(self):
        return self.department_name + "(" + self.campus.campus_name + ")"
    


class Degree(models.Model):
    education_level = models.CharField(
        "Education Level", max_length=255, help_text="Education Level E.g: Bachelors, Masters, PhD")
    degree_name = models.CharField(
        "Degree Name", max_length=255, help_text="Name Of Degree E.g: Computer Science(CS)")
