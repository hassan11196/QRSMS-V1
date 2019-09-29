from django.urls import path, include


from . import views

app_name='initial'


urlpatterns = [
    path('', views.index, name='index'),
    path('get_csrf',views.csrf,name="csrf_get"),
    path('ping_csrf', views.ping, name="csrf_ping"),
    path('temp_login',views.temp_login, name="temp_login"),
    path('test_student_login',views.StudentLoginView.as_view(), name="test_student_login"),
    path('test_student_login/<str:value>',views.StudentLoginView.as_view(), name="test_student_login2"),
    path('test_student_signup',views.StudentSignupView.as_view(), name="test_student_signup"),

 
]
