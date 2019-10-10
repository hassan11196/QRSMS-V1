import unittest
from django.urls import reverse
from django.test import Client
from .models import Course, Teacher, Faculty, Student, Semester
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_course(**kwargs):
    defaults = {}
    defaults["course_name"] = "course_name"
    defaults["course_code"] = "course_code"
    defaults.update(**kwargs)
    return Course.objects.create(**defaults)


def create_teacher(**kwargs):
    defaults = {}
    defaults["department"] = "department"
    defaults["nu_email"] = "nu_email"
    defaults.update(**kwargs)
    if "user" not in defaults:
        defaults["user"] = create_user()
    return Teacher.objects.create(**defaults)


def create_faculty(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    if "user" not in defaults:
        defaults["user"] = create_user()
    return Faculty.objects.create(**defaults)


def create_student(**kwargs):
    defaults = {}
    defaults["batch"] = "batch"
    defaults["arn"] = "arn"
    defaults["uid"] = "uid"
    defaults["degree_name_enrolled"] = "degree_name_enrolled"
    defaults["degree_short_enrolled"] = "degree_short_enrolled"
    defaults["department_name_enrolled"] = "department_name_enrolled"
    defaults["uni_mail"] = "uni_mail"
    defaults.update(**kwargs)
    if "user" not in defaults:
        defaults["user"] = create_user()
    return Student.objects.create(**defaults)


def create_semester(**kwargs):
    defaults = {}
    defaults["semester_year"] = "semester_year"
    defaults["start_date"] = "start_date"
    defaults["end_date"] = "end_date"
    defaults.update(**kwargs)
    if "teachers_available" not in defaults:
        defaults["teachers_available"] = create_teacher()
    return Semester.objects.create(**defaults)


class CourseViewTest(unittest.TestCase):
    '''
    Tests for Course
    '''
    def setUp(self):
        self.client = Client()

    def test_list_course(self):
        url = reverse('app_name_course_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_course(self):
        url = reverse('app_name_course_create')
        data = {
            "course_name": "course_name",
            "course_code": "course_code",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_course(self):
        course = create_course()
        url = reverse('app_name_course_detail', args=[course.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_course(self):
        course = create_course()
        data = {
            "course_name": "course_name",
            "course_code": "course_code",
        }
        url = reverse('app_name_course_update', args=[course.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TeacherViewTest(unittest.TestCase):
    '''
    Tests for Teacher
    '''
    def setUp(self):
        self.client = Client()

    def test_list_teacher(self):
        url = reverse('app_name_teacher_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_teacher(self):
        url = reverse('app_name_teacher_create')
        data = {
            "department": "department",
            "nu_email": "nu_email",
            "user": create_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_teacher(self):
        teacher = create_teacher()
        url = reverse('app_name_teacher_detail', args=[teacher.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_teacher(self):
        teacher = create_teacher()
        data = {
            "department": "department",
            "nu_email": "nu_email",
            "user": create_user().pk,
        }
        url = reverse('app_name_teacher_update', args=[teacher.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class FacultyViewTest(unittest.TestCase):
    '''
    Tests for Faculty
    '''
    def setUp(self):
        self.client = Client()

    def test_list_faculty(self):
        url = reverse('app_name_faculty_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_faculty(self):
        url = reverse('app_name_faculty_create')
        data = {
            "user": create_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_faculty(self):
        faculty = create_faculty()
        url = reverse('app_name_faculty_detail', args=[faculty.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_faculty(self):
        faculty = create_faculty()
        data = {
            "user": create_user().pk,
        }
        url = reverse('app_name_faculty_update', args=[faculty.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class StudentViewTest(unittest.TestCase):
    '''
    Tests for Student
    '''
    def setUp(self):
        self.client = Client()

    def test_list_student(self):
        url = reverse('app_name_student_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_student(self):
        url = reverse('app_name_student_create')
        data = {
            "batch": "batch",
            "arn": "arn",
            "uid": "uid",
            "degree_name_enrolled": "degree_name_enrolled",
            "degree_short_enrolled": "degree_short_enrolled",
            "department_name_enrolled": "department_name_enrolled",
            "uni_mail": "uni_mail",
            "user": create_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_student(self):
        student = create_student()
        url = reverse('app_name_student_detail', args=[student.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_student(self):
        student = create_student()
        data = {
            "batch": "batch",
            "arn": "arn",
            "uid": "uid",
            "degree_name_enrolled": "degree_name_enrolled",
            "degree_short_enrolled": "degree_short_enrolled",
            "department_name_enrolled": "department_name_enrolled",
            "uni_mail": "uni_mail",
            "user": create_user().pk,
        }
        url = reverse('app_name_student_update', args=[student.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class SemesterViewTest(unittest.TestCase):
    '''
    Tests for Semester
    '''
    def setUp(self):
        self.client = Client()

    def test_list_semester(self):
        url = reverse('app_name_semester_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_semester(self):
        url = reverse('app_name_semester_create')
        data = {
            "semester_year": "semester_year",
            "start_date": "start_date",
            "end_date": "end_date",
            "teachers_available": create_teacher().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_semester(self):
        semester = create_semester()
        url = reverse('app_name_semester_detail', args=[semester.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_semester(self):
        semester = create_semester()
        data = {
            "semester_year": "semester_year",
            "start_date": "start_date",
            "end_date": "end_date",
            "teachers_available": create_teacher().pk,
        }
        url = reverse('app_name_semester_update', args=[semester.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


