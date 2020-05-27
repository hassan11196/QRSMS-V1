from django.urls import path, include
from rest_framework import routers


from . import api
from . import views

student_portal = 'student_portal'

router = routers.DefaultRouter()
router.register(r'student', api.StudentViewSet)

urlpatterns = [
    # urls for Django Rest Framework API
    path('api/', include(router.urls)),
]


urlpatterns += [
    path('login/', views.StudentLoginView.as_view(), name="student_login"),
    path('logout/', views.StudentLogoutView.as_view(), name='student_logout'),
    path('home_json/', views.Home_json.as_view(), name='home_json'),
    # path('login/<str:value>',views.StudentLoginView.as_view(), name="test_student_login2"),
    path('signup/', views.StudentSignupView.as_view(), name="test_student_signup"),
    path('sections/', views.StudentSectionView.as_view(), name='student_section'),
    path('attendance/<str:course_code>/<str:section>/',
         views.StudentAttendanceView.as_view(), name='student_attendance'),
    path('registration/period_active/', views.RegistrationCheck.as_view(),
         name='stduent_registration_open'),
    path('registration/available_courses/', views.RegistrationCourses.as_view(),
         name='registration_available_courses'),
    path('timetable/', views.TimeTableView.as_view(), name='student_timetable'),
    path('postQR/', views.PostAttendanceQR.as_view(), name='student_post_qr'),
    path('getChallan/', views.get_challan, name="ChallanGenerate"),
    path('updateChallan/', views.update_challan, name="updateCHallan"),
    path('get_transcript/', views.Student_Transcript.as_view()),

]
