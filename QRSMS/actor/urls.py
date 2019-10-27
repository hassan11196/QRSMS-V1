from django.urls import path, include
from rest_framework import routers


from . import api
from . import views

actor = 'actor'
router = routers.DefaultRouter()


urlpatterns = [
    # urls for Django Rest Framework API
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('temp_login',views.temp_login, name="temp_login"),

]