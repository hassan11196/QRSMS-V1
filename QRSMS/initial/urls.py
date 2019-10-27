from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

initial='initial'
router = routers.DefaultRouter()
router.register(r'course', api.CourseViewSet)
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
    # urls for Semester
    path('initial/semester/', views.SemesterListView.as_view(), name='initial_semester_list'),
    path('initial/semester/create/', views.SemesterCreateView.as_view(), name='initial_semester_create'),
    path('initial/semester/detail/<int:pk>/', views.SemesterDetailView.as_view(), name='initial_semester_detail'),
    path('initial/semester/update/<int:pk>/', views.SemesterUpdateView.as_view(), name='initial_semester_update'),
)
urlpatterns += [
    path('', views.index, name='index'),
    path('get_csrf',views.csrf,name="csrf_get"),
    path('ping_csrf', views.ping, name="csrf_ping")
 
]
