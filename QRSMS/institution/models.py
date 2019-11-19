from django.db import models


# Create your models here.

class University(models.Model):
    class Meta:
        verbose_name_plural = "University"
    uni_id = models.AutoField(
        primary_key=True, name="uni_id", verbose_name="University Registration ID")
    name = models.CharField(
        max_length=255, help_text="Name of University")

    def __str__(self):
        return self.name
    

class Campus(models.Model):

    class Meta:
        verbose_name_plural = "Campuses"
        unique_together = ('campus_name','campus_city',)
    
    campus_id = models.AutoField(
        primary_key=True, name="campus_id", verbose_name="Campus ID")
    uni_name = models.ForeignKey("institution.University", on_delete=models.CASCADE,
                                 verbose_name="Universities Campus", help_text="A university can have many campuses")
    address = models.CharField(
        max_length=255, help_text="Address of Campus", name="campus_address")
    campus_name = models.CharField(
        max_length=255, help_text="Name of Campus of University", name='campus_name')
    campus_city = models.CharField(
        max_length=255, help_text="City Name of Campus", name='campus_city')
    contact_no = models.IntegerField(help_text='Contact Number of Campus', null=True, name='contact_no')
    contact_email = models.EmailField(help_text='Email of Campus', null=True, name = 'contact_email')

    campus_country = models.CharField(
        max_length=255, help_text="Country Name of Campus", null=True, name = 'campus_country')

    def __str__(self):
        return self.campus_name + " " + self.campus_city
    

class Department(models.Model):
    campus = models.ForeignKey(
        'institution.Campus', on_delete=models.CASCADE, related_name="Campuses_Department")
    department_id = models.PositiveIntegerField(
        "Department ID", help_text="Department ID" ,primary_key = True)
    department_name = models.CharField("Department Name", max_length=255, help_text="Name of Department of Campus", unique=True)

    department_hod = models.ForeignKey("actor.User", help_text="Current HOD of Department", name='department_hod', on_delete=models.SET_NULL, null=True)
    department_teachers = models.ManyToManyField("teacher_portal.Teacher", related_name='teachers_in_department')
    department_students = models.ManyToManyField("student_portal.Student", related_name='students_in_department')
    department_faculty = models.ManyToManyField("faculty_portal.Faculty", related_name='faculty_in_department')
    def __str__(self):
        return self.department_name + "(" + self.campus.campus_name + ")"
    


class Degree(models.Model):

    offering_department = models.ForeignKey('institution.Department', on_delete=models.SET_NULL, null=True)
    minimium_years_education = models.PositiveSmallIntegerField(null=True,name='minimium_years_education', help_text = 'minimium years of education required for admission in Degree')
    completion_year = models.PositiveSmallIntegerField(null=True,name='completion_year', help_text = 'Years of Education after completion of degree')
    duration = models.PositiveSmallIntegerField(null=True,name = 'duration', help_text = 'Duration of Degree Program')
    education_level = models.CharField(
        "Education Level",null=True, max_length=255, help_text="Education Level E.g: Bachelors, Masters, PhD")
    degree_name = models.CharField(
        "Degree Name", max_length=255,null=True, help_text="Name Of Degree E.g: Computer Science(CS)")
    degree_short = models.CharField(
        name = 'degree_short', max_length=255, help_text="Short name Of Degree E.g : CS, BBA", primary_key=True, default='DND')

    registrations_open = models.BooleanField(help_text = 'True if Course Registrations are Open, else False',default=False, blank=True, null=True)
    registration_semester = models.ForeignKey('initial.Semester',on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.degree_name + " " + self.degree_short
    
class BatchSection(models.Model):
    sec_batch = models.CharField(max_length=25, blank=True, null=True,help_text='pk')
    batch = models.CharField(max_length = 256)
    section = models.CharField(max_length = 10, help_text='Section Name Etc A,B,C etc')
    students = models.ManyToManyField('student_portal.Student')
    limit = models.SmallIntegerField(default=40, blank=True, null=True)


    def save(self, *args, **kwargs):
        print(self.batch, self.section, self.sec_batch)
        if self.sec_batch is None or self.batch + "-" + self.section != str(self.sec_batch):
            self.sec_batch = str(self.batch) + "-" + str(self.section)
        super(BatchSection, self).save(*args, **kwargs)
    
    
    class Meta:
        unique_together = ('batch','section')

    def __str__(self):
        return self.sec_batch
    

    @classmethod
    def fetch_all_students(cls):
        from student_portal.models import Student
        s = Student.objects.all()
        for student in s:
            s, created = cls.objects.get_or_create(section = student.admission_section, batch  = student.batch)
            if created:
                print(s)
