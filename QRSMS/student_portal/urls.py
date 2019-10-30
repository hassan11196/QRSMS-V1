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
    path('',views.Home_json.as_view(), name='faek_home_json'),
    path('login/',views.StudentLoginView.as_view(), name="test_student_login"),
    # path('login/<str:value>',views.StudentLoginView.as_view(), name="test_student_login2"),
    path('signup/',views.StudentSignupView.as_view(), name="test_student_signup"),
    path('home_json/',views.Home_json.as_view(), name='home_json')
 
]