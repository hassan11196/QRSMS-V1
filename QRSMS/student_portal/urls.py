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
    # path('',views.StudentListView.as_view(), name='student_portal_student_list'),
    path('login/',views.StudentLoginView.as_view(), name="student_login"),
    path('logout/',views.StudentLogoutView.as_view(), name='student_logout'),
    path('home_json/',views.Home_json.as_view(), name='home_json'),
    # path('login/<str:value>',views.StudentLoginView.as_view(), name="test_student_login2"),
    path('signup/',views.StudentSignupView.as_view(), name="test_student_signup"),
    path('registration_period_active/',views.RegistrationCheck.as_view(),name='stduent_registration_open')
    # path('create', views.StudentCreateView.as_view(), name='initial_student_create'),
    # path('detail/<int:pk>/', views.StudentDetailView.as_view(), name='initial_student_detail'),
    # path('update/<int:pk>/', views.StudentUpdateView.as_view(), name='initial_student_update'),
 
]