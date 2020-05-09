from django.urls import path, include
from rest_framework import routers


from . import api
from . import views
from . import models

actor = 'actor'
router = routers.DefaultRouter()
router.register('employee', api.EmployeeViewSet, basename='employee')

urlpatterns = [
    # urls for Django Rest Framework API
    # path('api/', include(router.urls)),
]

urlpatterns += [
    path('temp_login', views.temp_login, name="temp_login"),

]
