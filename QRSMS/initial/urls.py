from django.urls import path, include


from . import views

app_name='initial'


urlpatterns = [
    path('', views.index, name='index'),
    path('get_csrf',views.csrf,name="csrf_get"),
    path('ping_csrf', views.ping, name="csrf_ping")

 
]
