from django.urls import path, include
from rest_framework import routers


from . import api
from . import views

faculty_portal = 'faculty_portal'

router = routers.DefaultRouter()
router.register(r'faculty', api.FacultyViewSet)


urlpatterns = [
    # urls for Django Rest Framework API
    path('api/', include(router.urls)),
]


urlpatterns += (
    # urls for Faculty
    path('login/', views.FacultyLoginView.as_view(), name="faculty_login"),
    path('logout/', views.FacultyLogoutView.as_view(), name='Faculty_logout'),
    path('home_json/', views.Home_json.as_view(), name='home_json'),
    path('student-timetable/', views.GetStudentTimeTable.as_view(),
         name='student_timetable'),
    path('start-semester/', views.SemesterStart.as_view(), name='semester_start'),
    path('register-student/', views.RegisterStudent.as_view(),
         name='register_student')
)

