"""QRSMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from rest_framework import routers
import django_restful_admin
from rest_framework_swagger.views import get_swagger_view
from actor import views as actor_views
from student_portal import views as student_views
from teacher_portal import views as teacher_views
from faculty_portal import views as faculty_views
from initial import views



router = routers.DefaultRouter()
router.register(r'users', actor_views.UserViewSet)
router.register(r'groups', actor_views.GroupViewSet)
router.register(r'course_info',views.CourseViewSet)
router.register(r'students', student_views.StudentViewSet)
router.register(r'teachers', teacher_views.TeacherViewSet)

schema_view = get_swagger_view(title = 'QRSMS')
admin.site.site_header = 'QRSMS Admin Portal'
admin.site.site_title = "QRSMS"
admin.site.index_title = "Welcome to QRSMS Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view),
    path('', include('initial.urls')),
    path('actor/', include('actor.urls')),
    path(r'student/',include('student_portal.urls')),
    path('teacher/',include('teacher_portal.urls')),
    path('faculty/',include('faculty_portal.urls')),
    path('rest/', include(router.urls)),
    
    



    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'rest_admin/', django_restful_admin.site.urls),
    #re_path(r'^(?:.*)/?$', views.index), # URL Fallback to react router

]
