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


urlpatterns += (
    # urls for Student
    path('', views.StudentListView.as_view(), name='initial_student_list'),
    path('create', views.StudentCreateView.as_view(), name='initial_student_create'),
    path('detail/<int:pk>/', views.StudentDetailView.as_view(), name='initial_student_detail'),
    path('update/<int:pk>/', views.StudentUpdateView.as_view(), name='initial_student_update'),
)

urlpatterns += [
    path('test_student_login',views.StudentLoginView.as_view(), name="test_student_login"),
    path('test_student_login/<str:value>',views.StudentLoginView.as_view(), name="test_student_login2"),
    path('test_student_signup',views.StudentSignupView.as_view(), name="test_student_signup"),
    path('home_json',views.Home_json.as_view(), name='home_json')
 
]