from django.db import models
from django.db.models import F, Q
from django.core.validators import RegexValidator, ValidationError
from django.urls import reverse
from django.dispatch import receiver
import datetime
from institution.models import University, Campus, Degree
from institution.constants import UNIVERISTY_ID_REGEX
from actor.models import User, BATCH_YEAR_REGEX, SEMSESTER_CHOICES, STUDENT_YEAR_CHOICE
from student_portal.models import Student
from teacher_portal.models import Teacher
from faculty_portal.models import Faculty
from .signals import attendance_sheet_for_student, mark_sheet_for_student, student_info_section_for_student


ACADEMIC_YEAR = 2019

# Create your models here.


class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        (1, 'Core'),
        (2, 'Elective'),
        (3, 'Elective (X)')
    )
    course_name = models.CharField(max_length=50, name="course_name")
    course_code = models.CharField(
        max_length=20, primary_key=True, name="course_code")
    course_short = models.CharField(max_length=50)
    credit_hour = models.PositiveSmallIntegerField(
        name='credit_hour', null=True)
    pre_requisites = models.ManyToManyField(
        "initial.Course", name='pre_requisites', verbose_name="Prerequisite Courses")
    course_type = models.PositiveIntegerField(
        name='course_type', help_text="Core or Elective", choices=COURSE_TYPE_CHOICES)

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

    department = models.ForeignKey(
        'institution.Department', on_delete=models.SET_NULL, null=True)
    semester_code = models.CharField(
        max_length=255, primary_key=True, default='TEST2000')
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
    start_date = models.DateField(
        name="start_date", default=datetime.date.today)
    end_date = models.DateField(name="end_date", default=datetime.date.today)
    teachers_available = models.ManyToManyField(
        Teacher, related_name="teachers_available")
    students_registered = models.ManyToManyField(
        Student, related_name="students_registered")

    regular_course_load = models.ManyToManyField(
        'initial.RegularCoreCourseLoad')
    elective_course_load = models.ManyToManyField(
        'initial.RegularElectiveCourseLoad')
    degree_short = models.CharField(max_length=30, null=True, blank=True)
    fee_per_CR = models.FloatField(
        max_length=10, null=True, blank=True, default=7400)
    current_semester = models.BooleanField(default=False)

    class Meta:
        unique_together = ('semester_season', 'semester_year')
        ordering = ['-semester_code']
        get_latest_by = 'start_date'

    def __str__(self):
        return self.semester_code

    def save(self, *args, **kwargs):
        try:
            deg = Degree.objects.get(degree_short=self.degree_short)
            if deg:
                deg.registrations_open = True
                deg.registration_semester = self
                deg.save()
        except Degree.DoesNotExist as e:
            print(e)
            raise ValueError("Semester Not Created")
        # Call the real save() method
        super(Semester, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('initial_semester_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('initial_semester_update', args=(self.pk,))

    def make_semester(self):
        rg = self.regular_course_load.all()[0]
        for c in rg.courses.all():
            make_classes(semester_code=self.semester_code,
                         course_code=c.course_code, sections=['A', 'B', 'C', 'D', 'E'])

    def pre_offer(self):
        for rg in self.regular_course_load.all():
            students = Student.objects.filter(student_year=rg.student_year)
            for s in students:
                # One time only for student
                of_courses = OfferedCourses(
                    student=s, semester_code=self.semester_code)
                of_courses.save()

    def offer_core_courses(self):
        for rg in self.regular_course_load.all():
            students = Student.objects.filter(student_year=rg.student_year)
            for s in students:
                of_courses = OfferedCourses.objects.get(
                    student=s, semester_code=self.semester_code)

                for c in rg.courses.all():
                    course_status = CourseStatus(
                        course=c, section=s.admission_section)
                    course_status.save()
                    if of_courses.courses_offered is None:
                        of_courses.courses_offered = course_status
                    else:
                        of_courses.courses_offered.add(course_status)
                of_courses.save()

    def offer_elective_courses(self):
        for eg in self.elective_course_load.all():
            students = Student.objects.filter(student_year=eg.student_year)
            for s in students:
                of_courses = OfferedCourses.objects.get(
                    student=s, semester_code=self.semester_code)

                for c in eg.courses.all():
                    course_status = CourseStatus(course=c, section='GR1')
                    course_status.save()
                    if of_courses.courses_offered is None:
                        of_courses.courses_offered = course_status
                    else:
                        of_courses.courses_offered.add(course_status)
                of_courses.save()


class StudentInfoSection(models.Model):
    student = models.ForeignKey(
        'student_portal.Student', on_delete=models.SET_NULL, blank=True, null=True)
    attendance_sheet = models.ForeignKey(
        'initial.AttendanceSheet', on_delete=models.SET_NULL, blank=True, null=True)
    mark_sheet = models.ForeignKey(
        'initial.MarkSheet', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.student.uid + "_" + (self.coursesection_set.first().scsddc if self.coursesection_set.first() != None else 'NO COURSE SECTION')


class CourseSection(models.Model):
    class Meta:
        ordering = ['-scsddc']

    semester_code = models.CharField(
        max_length=256, name='semester_code', help_text='semester code - SDDC', blank=True, null=True)
    course_code = models.CharField(
        max_length=256, name='course_code', blank=True, null=True)
    course = models.ForeignKey(
        'initial.Course', on_delete=models.SET_NULL, null=True)
    SCSDDC = models.CharField(
        max_length=256, blank=True, null=True, name='scsddc')

    section_total_seats = models.PositiveIntegerField(
        blank=True, null=True, default=40, help_text='Total Seats : Seats Left + students Registered')
    section_seats = models.PositiveIntegerField(
        blank=True, null=True, default=40, help_text='Seats Left')

    students_count = models.PositiveIntegerField(
        blank=True, null=True, default=True)
    section_name = models.CharField(max_length=256, blank=True, null=True)

    student_info = models.ManyToManyField(
        'initial.StudentInfoSection')

    teacher = models.ForeignKey(
        'teacher_portal.Teacher', on_delete=models.SET_NULL, null=True)

    average = models.PositiveIntegerField(blank=True, null=True, default=0)
    standard_devition = models.PositiveIntegerField(
        blank=True, null=True, default=0)
    minimum = models.PositiveIntegerField(blank=True, null=True, default=0)
    maximum = models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.section_name + "_" + self.course_code + "_" + self.semester_code

    def calculate_class_marks(self):
        pass

    @classmethod
    def set_scsddc(cls):
        all_sections = cls.objects.exclude(
            scsddc__isnull=True, scsddc__exact='')
        for section in all_sections:
            section.scsddc = section.section_name + "_" + \
                section.course_code + "_" + section.semester_code
            section.save()


class CourseClass(models.Model):
    semester_code = models.CharField(
        max_length=256, name='semester_code', help_text='semester code - SDDC', blank=True, null=True)
    course_code = models.CharField(
        max_length=256, name='course_code', blank=True, null=True)
    CSDDC = models.CharField(max_length=256, blank=True, null=True)

    course = models.ForeignKey(
        'initial.Course', on_delete=models.SET_NULL, null=True)
    sections = models.ManyToManyField('initial.CourseSection')
    teachers = models.ManyToManyField('teacher_portal.Teacher')
    course_coordinator = models.ForeignKey(
        'teacher_portal.Teacher', on_delete=models.SET_NULL, null=True, related_name='course_coordinator_CourseClass')

    def __str__(self):
        return self.course_code + "_" + self.semester_code


class SectionAttendance(models.Model):

    ATTENDANCE_SLOTS = (
        (1, '8:00 AM - 9:00'),
        (2, '9:00 AM- 10:00'),
        (3, '10:00 AM- 11:00 PM'),
        (4, '11:00 AM- 12:00 PM'),
        (5, '12:00 PM- 1:00 PM'),
        (6, '1:00 PM- 2:00 PM'),
        (7, '2:00 PM- 3:00 PM'),
        (8, '3:00 PM- 4:00 PM'),
    )

    class_date = models.DateField(
        default=datetime.date.today, null=True, blank=True)
    attendance_slot = models.CharField(
        choices=ATTENDANCE_SLOTS, max_length=256, blank=True, null=True)
    attendance_time_start = models.TimeField(
        auto_now_add=True, null=True, blank=True)
    attendance_interval_allowed = models.PositiveSmallIntegerField(
        null=True, blank=True, default=30)
    qr_change_interval = models.PositiveSmallIntegerField(
        null=True, blank=True, default=1800)

    duration_hour = models.SmallIntegerField(default=1, null=True, blank=True)
    SCSDDC = models.CharField(
        max_length=256, name='scsddc', null=True, blank=True)
    section = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        unique_together = ('scsddc', 'class_date',
                           'attendance_slot', 'section')

    def __str__(self):
        return str(self.class_date) + "_" + self.attendance_slot + "_" + self.scsddc


class SectionMarks(models.Model):
    marks_type = models.CharField(max_length=256)
    total_marks = models.FloatField(null=True, blank=True)
    weightage = models.FloatField(null=True, blank=True)
    SCSDDC = models.CharField(
        max_length=256, name='scsddc', null=True, blank=True)
    section = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        unique_together = ('scsddc', 'marks_type', 'section')

    def __str__(self):
        return self.marks_type + "_" + self.scsddc


class StudentAttendance(models.Model):
    ATTENDANCE_STATES = (
        ('NR', 'Not Registered'),
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),  # late
        ('LV', 'Leave')
    )
    ATTENDANCE_SLOTS = (
        (1, '8:00 AM - 9:00'),
        (2, '9:00 AM- 10:00'),
        (3, '10:00 AM- 11:00 PM'),
        (4, '11:00 AM- 12:00 PM'),
        (5, '12:00 PM- 1:00 PM'),
        (6, '1:00 PM- 2:00 PM'),
        (7, '2:00 PM- 3:00 PM'),
        (8, '3:00 PM- 4:00 PM'),
    )

    student = models.ForeignKey(
        "student_portal.Student", on_delete=models.SET_NULL, null=True)
    class_date = models.DateField(
        name='class_date', blank=True, null=True, default=datetime.date.today)
    attendance_slot = models.CharField(
        choices=ATTENDANCE_SLOTS, max_length=256, blank=True, null=True)
    state = models.CharField(choices=ATTENDANCE_STATES,
                             max_length=256, default='NR')
    attendance_marked_time = models.TimeField(null=True, blank=True)

    duration_hour = models.SmallIntegerField(default=1, null=True, blank=True)
    attendance_type = models.CharField(choices=(
        ('M', 'Manual'), ('QR', 'QR-Code')), max_length=256, blank=True, null=True)
    SCSDDC = models.CharField(
        max_length=256, name='scsddc', null=True, blank=True)
    section = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'scsddc', 'class_date',
                           'attendance_slot', 'section')

    def __str__(self):
        return self.student.uid + "_" + str(self.class_date) + "_" + self.attendance_slot


class StudentMarks(models.Model):
    MARK_TYPE = (
        ('F', 'Final'),
        ('M', 'Mid'),
        ('Q', 'Quiz'),
        ('A', 'Assignment'),
        ('CP', 'Class Participation'),
        ('L', 'Lab Marks')
    )
    student = models.ForeignKey(
        "student_portal.Student", on_delete=models.SET_NULL, null=True)
    #mark_type = models.CharField(max_length=256, choices=MARK_TYPE,blank=True, null=True)
    mark_type = models.CharField(max_length=256, blank=True, null=True)
    obtained_marks = models.FloatField(blank=True, null=True)
    total_marks = models.FloatField(blank=True, null=True)
    weightage = models.FloatField(null=True, blank=True)
    SCSDDC = models.CharField(
        max_length=256, name='scsddc', null=True, blank=True)


# Attendace Sheet of a Single Student, with SDDC Semester_Dep_Deg_Campus
class AttendanceSheet(models.Model):
    student = models.ForeignKey(
        "student_portal.Student", on_delete=models.SET_NULL, null=True, blank=True)
    SCSDDC = models.CharField(
        max_length=256, name='scsddc', null=True, blank=True)
    attendance = models.ManyToManyField(
        'initial.StudentAttendance', blank=True)

    def __str__(self):
        return self.student.uid + "_" + self.scsddc

    class Meta:
        unique_together = ('student', 'scsddc')

# def get_attendance_table(table_name):
#     class ClassAttendanceSheetMeta(models.base.ModelBase):
#         def __new__(cls, name, bases, attrs):
#             model = super(ClassAttendanceSheetMeta, cls).__new__(cls,name,bases,attrs)
#             model._meta.db_table = table_name
#             return model


#     class AttendanceSheet(models.Model):
#         __metaclass__ = ClassAttendanceSheetMeta
#         student = models.ForeignKey("student_portal.Student", on_delete=models.SET_NULL, null=True)
#         SDDC = models.CharField(max_length=256, name='sddc', null=True)
#         attendance = models.ManyToManyField('initial.Attendance')
#     return AttendanceSheet

class MarkSheet(models.Model):
    student = models.ForeignKey(
        "student_portal.Student", on_delete=models.SET_NULL, null=True)
    SCSDDC = models.CharField(max_length=256, name='scsddc', null=True)
    Marks = models.ManyToManyField('initial.StudentMarks')
    grand_total_marks = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.student.uid + "_" + self.scsddc

    class Meta:
        unique_together = ('student', 'scsddc')


class RegularCoreCourseLoad(models.Model):
    semester_season = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    courses = models.ManyToManyField(Course)
    degree = models.ForeignKey(
        'institution.Degree', on_delete=models.SET_NULL, null=True)
    credit_hour_limit = models.PositiveSmallIntegerField(
        name='credit_hour_limit', default=19)
    student_year = models.SmallIntegerField(
        choices=STUDENT_YEAR_CHOICE, name='student_year', null=True)

    def __str__(self):
        return SEMSESTER_CHOICES[self.semester_season - 1][1]+"-"+STUDENT_YEAR_CHOICE[self.student_year-1][1]


class RegularElectiveCourseLoad(models.Model):
    semester_season = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    courses = models.ManyToManyField(Course)
    student_year = models.SmallIntegerField(
        choices=STUDENT_YEAR_CHOICE, name='student_year', null=True)

    def __str__(self):
        return 'Electives : ' + SEMSESTER_CHOICES[self.semester_season - 1][1] + "-"+STUDENT_YEAR_CHOICE[self.student_year-1][1]


# Relegated to Later Versions
class RepeatCourseLoad(models.Model):
    semester_season = models.SmallIntegerField(
        choices=SEMSESTER_CHOICES, name="semester_season")
    core_coursess = models.ManyToManyField('initial.RegularCoreCourseLoad')
    elective_courses = models.ManyToManyField(
        'initial.RegularElectiveCourseLoad')


class CourseStatus(models.Model):
    course = models.ForeignKey(
        'initial.course', related_name='course_status_offer', on_delete=models.CASCADE)
    status = models.CharField(choices=(('R', 'Registered'), ('NR', 'Not Registered')),
                              blank=True, null=True, max_length=256, default='NR')
    section = models.CharField(max_length=256, blank=True, null=True)
    one_time_field = models.BooleanField(
        blank=True, null=True, default=False, help_text='Used for First Time Registration.')

    def __str__(self):
        return self.offeredcourses_set.get().student.uid + "_" + self.course.course_name + "_" + self.status

    def save(self, *args, **kwargs):
        course_section = CourseSection.objects.get(
            section_name=self.section, course_code=self.course.course_code, semester_code=self.offeredcourses_set.get().semester_code)
        if course_section is None:
            raise CourseSection.DoesNotExist
        if self.status == 'R':
            course_section.section_seats = F('section_seats') - 1
            course_section.students_count = F('students_count') + 1

            print("Sending Signal")
            info = student_info_section_for_student.send(sender=self, student=self.offeredcourses_set.get(
            ).student, course_section=course_section, option='create')

            print(info)

        elif self.status == 'NR':
            course_section.section_seats = F('section_seats') + 1
            course_section.students_count = F('students_count') - 1
            print("Sending Signal")
            info = student_info_section_for_student.send(sender=self, student=self.offeredcourses_set.get(
            ).student, course_section=course_section, option='delete')
            print(info)

        course_section.save()
        # Call the real save() method
        super(CourseStatus, self).save(*args, **kwargs)


class OfferedCourses(models.Model):
    semester_code = models.CharField(
        max_length=256, name='semester_code', help_text='semester code - SDDC', blank=True, null=True)
    student = models.ForeignKey(
        'student_portal.Student', related_name='offered_courses', on_delete=models.SET_NULL, null=True)
    courses_offered = models.ManyToManyField('initial.CourseStatus')

    class Meta:
        unique_together = ('semester_code', 'student', )

    def __str__(self):
        return self.student.uid + "_" + self.semester_code

# course_code -> of course
# teachers_assigned -> to sections
# course_coordinator -> of course
# students_registered -> in semester


def make_classes(semester_code, course_code, sections):
    section_list = []
    for section in sections:
        course_section = CourseSection(
            semester_code=semester_code, course_code=course_code, section_name=section, course=Course.objects.get(course_code=course_code))
        course_section.save()
        section_list.append(course_section)

    course_class = CourseClass(semester_code=semester_code, course_code=course_code,
                               course=Course.objects.get(course_code=course_code))
    course_class.save()
    print(course_class)
    for section in section_list:
        if course_class.sections is None:
            course_class.sections = section
        else:
            course_class.sections.add(section)


@receiver(student_info_section_for_student)
def make_or_delete_student_info_section_for_student(**kwargs):
    if kwargs['option'] == 'create':
        print('Received Signal For Creation Student Info Section')
        SCSDDC_temp = str(kwargs['course_section'])
        new_sheet_attendance = AttendanceSheet.objects.get_or_create(
            student=kwargs['student'], scsddc=SCSDDC_temp)[0]
        new_sheet_marks = MarkSheet.objects.get_or_create(
            student=kwargs['student'], scsddc=SCSDDC_temp)[0]

        new_sheet_marks.save()
        new_sheet_attendance.save()

        info = StudentInfoSection(
            student=kwargs['student'], mark_sheet=new_sheet_marks, attendance_sheet=new_sheet_attendance)

        info.save()

        csection = CourseSection.objects.get(scsddc=SCSDDC_temp)
        print(csection)
        if csection.student_info is None:
            csection.student_info = info
        else:
            csection.student_info.add(info)
        csection.save()

        return 'Success'
    else:
        print('Received Signal For Deletion Student Info Section')
        SCSDDC_temp = str(kwargs['course_section'])
        info = StudentInfoSection.objects.get(student=kwargs['student'])
        info.mark_sheet.delete()
        info.attendance_sheet.delete()

        csection = CourseSection.objects.get(scsddc=SCSDDC_temp)
        csection.student_info.remove(info)
        info.delete()
        csection.save()
        return 'Success'


# @receiver(attendance_sheet_for_student)
# def make_or_delete_attendance_sheet_for_student(**kwargs):
#     if kwargs['option'] == 'create':
#         print('Received Signal For Creation Attendance Sheet')
#         SCSDDC_temp = str(kwargs['course_section'])
#         new_sheet = AttendanceSheet(
#             student=kwargs['student'], scsddc=SCSDDC_temp)
#         new_sheet.save()
#         csection = CourseSection.objects.get(scsddc=SCSDDC_temp)
#         csection.attendance_sheet.add(new_sheet)
#         csection.save()
#         return 'Success'
#     else:
#         print('Received Signal For Deletion Attendance Sheet')
#         SCSDDC_temp = str(kwargs['course_section'])
#         new_sheet = AttendanceSheet.objects.get(
#             student=kwargs['student'], scsddc=SCSDDC_temp)
#         csection = CourseSection.objects.get(scsddc=SCSDDC_temp)
#         csection.attendance_sheet.remove(new_sheet)
#         new_sheet.delete()
#         csection.save()
#         return 'Success'

# @receiver(mark_sheet_for_student)
# def make_or_delete_mark_sheet_for_student(**kwargs):
#     if kwargs['option'] == 'create':
#         print('Received Signal For Creation Mark Sheet')
#         SCSDDC_temp = str(kwargs['course_section'])
#         new_sheet = MarkSheet(student = kwargs['student'], scsddc = SCSDDC_temp)

#         new_sheet.save()
#         csection = CourseSection.objects.get(scsddc = SCSDDC_temp)
#         csection.mark_sheet.add(new_sheet)
#         print('Marksheet create')
#         print(csection.mark_sheet.all())
#         csection.save()
#         return 'Success'
#     else:
#         print('Received Signal For Deletion Attendance Sheet')
#         SCSDDC_temp = str(kwargs['course_section'])

#         new_sheet = MarkSheet.objects.get(student = kwargs['student'], scsddc = SCSDDC_temp)
#         csection = CourseSection.objects.get(scsddc = SCSDDC_temp)
#         csection.mark_sheet.remove(new_sheet)
#         new_sheet.delete()
#         csection.save()
#         return 'Success'
