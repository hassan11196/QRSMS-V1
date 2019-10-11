from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

initial='initial'
router = routers.DefaultRouter()
router.register(r'course', api.CourseViewSet)
router.register(r'teacher', api.TeacherViewSet)
router.register(r'faculty', api.FacultyViewSet)
router.register(r'student', api.StudentViewSet)
router.register(r'semester', api.SemesterViewSet)

urlpatterns = [
    # urls for Django Rest Framework API
    path('api/', include(router.urls)),
]
urlpatterns += (
    # urls for Course
    path('initial/course/', views.CourseListView.as_view(), name='initial_course_list'),
    path('initial/course/create/', views.CourseCreateView.as_view(), name='initial_course_create'),
    path('initial/course/detail/<int:pk>/', views.CourseDetailView.as_view(), name='initial_course_detail'),
    path('initial/course/update/<int:pk>/', views.CourseUpdateView.as_view(), name='initial_course_update'),
)

urlpatterns += (
    # urls for Teacher
    path('initial/teacher/', views.TeacherListView.as_view(), name='initial_teacher_list'),
    path('initial/teacher/create/', views.TeacherCreateView.as_view(), name='initial_teacher_create'),
    path('initial/teacher/detail/<int:pk>/', views.TeacherDetailView.as_view(), name='initial_teacher_detail'),
    path('initial/teacher/update/<int:pk>/', views.TeacherUpdateView.as_view(), name='initial_teacher_update'),
)

urlpatterns += (
    # urls for Faculty
    path('initial/faculty/', views.FacultyListView.as_view(), name='initial_faculty_list'),
    path('initial/faculty/create/', views.FacultyCreateView.as_view(), name='initial_faculty_create'),
    path('initial/faculty/detail/<int:pk>/', views.FacultyDetailView.as_view(), name='initial_faculty_detail'),
    path('initial/faculty/update/<int:pk>/', views.FacultyUpdateView.as_view(), name='initial_faculty_update'),
)

urlpatterns += (
    # urls for Student
    path('initial/student/', views.StudentListView.as_view(), name='initial_student_list'),
    path('initial/student/create/', views.StudentCreateView.as_view(), name='initial_student_create'),
    path('initial/student/detail/<int:pk>/', views.StudentDetailView.as_view(), name='initial_student_detail'),
    path('initial/student/update/<int:pk>/', views.StudentUpdateView.as_view(), name='initial_student_update'),
)

urlpatterns += (
    # urls for Semester
    path('initial/semester/', views.SemesterListView.as_view(), name='initial_semester_list'),
    path('initial/semester/create/', views.SemesterCreateView.as_view(), name='initial_semester_create'),
    path('initial/semester/detail/<int:pk>/', views.SemesterDetailView.as_view(), name='initial_semester_detail'),
    path('initial/semester/update/<int:pk>/', views.SemesterUpdateView.as_view(), name='initial_semester_update'),
)
urlpatterns += [
    path('', views.index, name='index'),
    path('get_csrf',views.csrf,name="csrf_get"),
    path('ping_csrf', views.ping, name="csrf_ping"),
    path('temp_login',views.temp_login, name="temp_login"),
    path('test_student_login',views.StudentLoginView.as_view(), name="test_student_login"),
    path('test_student_login/<str:value>',views.StudentLoginView.as_view(), name="test_student_login2"),
    path('test_student_signup',views.StudentSignupView.as_view(), name="test_student_signup"),
    path('home_json',views.Home_json.as_view(), name='home_json')
 
]
