from django.urls import path, include


from . import views

app_name='initial'


urlpatterns = [
    path('', views.index, name='index'),
 
]
