from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

initial='initial'
router = routers.DefaultRouter()
router.register(r'course', api.CourseViewSet)
router.register(r'semester', api.SemesterViewSet)
router.register(r'offeredcourses', api.OfferedCoursesViewSet)
router.register(r'coursestatus', api.CourseStatusViewSet)
router.register(r'attendance_sheet',api.AttendanceSheetViewSet)

urlpatterns = [
    # urls for Django Rest Framework API
    path('api/', include(router.urls)),
]
# urlpatterns += (
#     # urls for Course
#     path('initial/course/', views.CourseListView.as_view(), name='initial_course_list'),
#     path('initial/course/create/', views.CourseCreateView.as_view(), name='initial_course_create'),
#     path('initial/course/detail/<int:pk>/', views.CourseDetailView.as_view(), name='initial_course_detail'),
#     path('initial/course/update/<int:pk>/', views.CourseUpdateView.as_view(), name='initial_course_update'),
# )

# urlpatterns += (
#     # urls for Semester
#     path('initial/semester/', views.SemesterListView.as_view(), name='initial_semester_list'),
#     path('initial/semester/create/', views.SemesterCreateView.as_view(), name='initial_semester_create'),
#     path('initial/semester/detail/<int:pk>/', views.SemesterDetailView.as_view(), name='initial_semester_detail'),
#     path('initial/semester/update/<int:pk>/', views.SemesterUpdateView.as_view(), name='initial_semester_update'),
# )
urlpatterns += [
    path('', views.index, name='index'),
    path('management/get_csrf',views.csrf,name="csrf_get"),
    path('management/ping_csrf', views.ping, name="csrf_ping"),
    path('management/user_not_logged/', views.UserNotLogged.as_view(), name = 'user_not_loggged'),
    path('management/add_students/', views.Add_students.as_view(), name='manage_add_students'),
    path('management/add_semestercore/', views.Add_semesterCore.as_view(), name='manage_add_semsterCore'),
    path('management/add_university/', views.Add_university.as_view(), name = 'manage_add_university'),
    path('management/add_superuser/', views.Add_superuser.as_view(), name = 'manage_add_superuser'),
    path('management/add_courses/', views.Add_courses.as_view(), name = 'manage_add_courses'),
    path('management/add_campuses/', views.AddCampuses.as_view(), name = 'manage_add_campuses')
 
]
