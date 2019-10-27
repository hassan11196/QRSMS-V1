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
    path('', views.FacultyListView.as_view(), name='initial_faculty_list'),
    path('create', views.FacultyCreateView.as_view(), name='initial_faculty_create'),
    path('detail/<int:pk>/', views.FacultyDetailView.as_view(), name='initial_faculty_detail'),
    path('update/<int:pk>/', views.FacultyUpdateView.as_view(), name='initial_faculty_update'),
)



urlpatterns += [
    # path('temp_login',views.temp_login, name="temp_login"),
    # path('test_student_login',views.StudentLoginView.as_view(), name="test_student_login"),
    # path('test_student_login/<str:value>',views.StudentLoginView.as_view(), name="test_student_login2"),
    # path('test_student_signup',views.StudentSignupView.as_view(), name="test_student_signup"),
    # path('home_json',views.Home_json.as_view(), name='home_json')
 
]