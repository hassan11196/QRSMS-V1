from django.db import models


# Create your models here.

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
        'institution.Campus', on_delete=models.CASCADE, related_name="Campuses_Department")
    department_id = models.PositiveIntegerField(
        "Department ID", help_text="Department ID" ,primary_key = True)
    department_name = models.CharField("Department Name", max_length=255, help_text="Name of Department of Campus")

    def __str__(self):
        return self.department_name + "(" + self.campus.campus_name + ")"
    


class Degree(models.Model):
    minimium_years_education = models.PositiveSmallIntegerField(null=True,name='minimium_years_education', help_text = 'minimium years of education required for admission in Degree')
    completion_year = models.PositiveSmallIntegerField(null=True,name='completion_year', help_text = 'Years of Education after completion of degree')
    duration = models.PositiveSmallIntegerField(null=True,name = 'duration', help_text = 'Duration of Degree Program')
    education_level = models.CharField(
        "Education Level",null=True, max_length=255, help_text="Education Level E.g: Bachelors, Masters, PhD")
    degree_name = models.CharField(
        "Degree Name", max_length=255,null=True, help_text="Name Of Degree E.g: Computer Science(CS)")
    degree_short = models.CharField(
        name = 'degree_short', max_length=255, help_text="Short name Of Degree E.g : CS, BBA", primary_key=True, default='DND')

    def __str__(self):
        return self.degree_name + " " + self.degree_short
    
