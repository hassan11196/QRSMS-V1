from django.db import models

from django.core.validators import RegexValidator, ValidationError
from django.urls import reverse
from institution.models import University, Campus, Degree
from institution.constants import UNIVERISTY_ID_REGEX
from actor.models import User, BATCH_YEAR_REGEX, SEMSESTER_CHOICES, STUDENT_YEAR_CHOICE
from student_portal.models import Student
from teacher_portal.models import Teacher
from faculty_portal.models import Faculty


ACADEMIC_YEAR = 2019

# Create your models here.

class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        (1,'Core'),
        (2,'Elective'),
        (3,'Elective (X)')
    )
    course_name = models.CharField(max_length=50, name="course_name")
    course_code = models.CharField(
        max_length=20, primary_key=True, name="course_code")
    course_short = models.CharField(max_length=50)
    credit_hour = models.PositiveSmallIntegerField(name='credit_hour', null=True)
    pre_requisites = models.ManyToManyField("initial.Course",name='pre_requisites', verbose_name="Prerequisite Courses")
    course_type = models.PositiveIntegerField(name='course_type', help_text = "Core or Elective", choices=COURSE_TYPE_CHOICES)

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ('-pk',)

    def get_absolute_url(self):
        return reverse('initial_course_detail', args=(self.course_code,))


    def get_update_url(self):
        return reverse('initial_course_update', args=(self.course_code,))

# class Student(models.Model):
#     student_id = models.CharField(max_length=8,primary_key=True, validators = [RegexValidator("^[A-Z][0-9]{2}-[0-9]{4}$", message = "Invalid Student ID")], name="student_id_n")
      

class Semester(models.Model):

    department = models.ForeignKey('institution.Department', on_delete = models.SET_NULL, null=True)
    semester_code = models.CharField(max_length=255, primary_key=True , default='TEST2000')
    # offered_courses = models.ManyToManyField(
    #     Course, related_name="semester_offered")
    SEMSESTER_CHOICES = (
        (1, "FALL"),
        (2, "SPRING"),
        (3, "SUMMER")
    )
    semester_season = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    semester_year = models.IntegerField(name="semester_year")
    start_date = models.DateField(name="start_date")
    end_date = models.DateField(name="end_date")
    teachers_available = models.ManyToManyField(
        Teacher, related_name="teachers_available")
    students_registered = models.ManyToManyField(
        Student, related_name="students_registered")

    regular_course_load = models.ManyToManyField('initial.RegularCoreCourseLoad')
    elective_course_load = models.ManyToManyField('initial.RegularElectiveCourseLoad')
    degree_short = models.CharField(max_length=30, null=True, blank = True)
    class Meta:
        unique_together = ('semester_season', 'semester_year')
    
    def __str__(self):
        return self.semester_code
    
    def save(self, *args, **kwargs):
        try:
            deg = Degree.objects.get(degree_short = self.degree_short) 
            if deg:
                deg.registrations_open = True
                deg.registration_semester = self
                deg.save()
        except Degree.DoesNotExist as e:
            print(e)
            raise ValueError("Semester Not Created")
        super(Semester, self).save(*args, **kwargs) # Call the real save() method



    def get_absolute_url(self):
        return reverse('initial_semester_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('initial_semester_update', args=(self.pk,))

class CourseSection(models.Model):
    students = models.ManyToManyField('student_portal.Student')
    attendance_sheet = models.ManyToManyField('initial.AttendanceSheet')
    mark_sheet = models.ManyToManyField('initial.MarkSheet')
    teacher = models.ForeignKey('teacher_portal.Teacher', on_delete = models.SET_NULL, null =True)
    
    average = models.PositiveIntegerField(blank=True, null=True)
    standard_devition = models.PositiveIntegerField(blank=True, null=True)
    minimum = models.PositiveIntegerField(blank=True, null=True)
    maximum = models.PositiveIntegerField(blank=True, null=True)

    def calculate_class_marks(self):
        pass
    


class CourseClass(models.Model):
    course_code = models.ForeignKey('initial.Course', on_delete=models.SET_NULL, null = True)
    sections = models.ManyToManyField('initial.CourseSection')
    teachers = models.ManyToManyField('teacher_portal.Teacher')
    course_coordinator = models.ForeignKey('teacher_portal.Teacher', on_delete = models.SET_NULL, null=True, related_name='course_coordinator_CourseClass')


class Attendance(models.Model):
    ATTENDANCE_STATES = (
        ('NR', 'Not Registered'),
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'), # late
        ('LV', 'Leave')
    )
    student = models.ForeignKey("student_portal.Student", on_delete=models.SET_NULL, null=True)
    class_date = models.DateField()
    state = models.CharField(choices=ATTENDANCE_STATES, max_length=256, default='NR')
    attendance_time = models.TimeField()
    duration = models.SmallIntegerField(default=1)

class Marks(models.Model):
    MARK_TYPE = (
        ('F','Final'),
        ('M','Mid'),
        ('Q','Quiz'),
        ('A','Assignment'),
        ('CP','Class Participation'),
        ('L','Lab Marks')
    )
    student = models.ForeignKey("student_portal.Student", on_delete=models.SET_NULL, null=True)
    mark_type = models.CharField(max_length=256, choices=MARK_TYPE,blank=True, null=True)
    obtained_marks = models.PositiveIntegerField(blank=True, null=True)
    total_marks = models.PositiveIntegerField(blank=True, null=True)
    

# Attendace Sheet of a Single Student, with SDDC Semester_Dep_Deg_Campus
class AttendanceSheet(models.Model):
    student = models.ForeignKey("student_portal.Student", on_delete=models.SET_NULL, null=True)
    SDDC = models.CharField(max_length=256, name='sddc', null=True)
    attendance = models.ManyToManyField('initial.Attendance')


def get_attendance_table(table_name):
    class ClassAttendanceSheet(models.Model):
        class Meta:
            db_table = table_name

class MarkSheet(models.Model):
    student = models.ForeignKey("student_portal.Student", on_delete=models.SET_NULL, null=True)
    SDDC = models.CharField(max_length=256, name='sddc', null=True)
    Marks = models.ManyToManyField('initial.Marks')
    grand_total_marks = models.PositiveIntegerField(blank=True, null=True)
    

class RegularCoreCourseLoad(models.Model):
    semester_season = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    courses = models.ManyToManyField(Course)
    degree = models.ForeignKey('institution.Degree', on_delete=models.SET_NULL, null=True)
    credit_hour_limit = models.PositiveSmallIntegerField(name='credit_hour_limit', default=19)
    student_year = models.SmallIntegerField(choices=STUDENT_YEAR_CHOICE, name='student_year', null=True)    

    def __str__(self):
        return SEMSESTER_CHOICES[self.semester_season - 1][1]+"-"+STUDENT_YEAR_CHOICE[self.student_year-1][1]

class RegularElectiveCourseLoad(models.Model):
    semester_season = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    courses = models.ManyToManyField(Course)
    

    def __str__(self):
        return 'Electives : ' + SEMSESTER_CHOICES[self.semester_season - 1][1]
    

# Relegated to Later Versions
class RepeatCourseLoad(models.Model):
    semester_season = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    core_coursess = models.ManyToManyField('initial.RegularCoreCourseLoad')
    elective_courses = models.ManyToManyField('initial.RegularElectiveCourseLoad')