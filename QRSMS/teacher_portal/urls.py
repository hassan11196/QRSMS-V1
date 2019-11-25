from django.urls import path, include
from rest_framework import routers


from . import api
from . import views

teacher_portal = 'teacher_portal'


router = routers.DefaultRouter()
router.register(r'teacher', api.TeacherViewSet)

urlpatterns = [
    # urls for Django Rest Framework API
    path('api/', include(router.urls)),
]

urlpatterns += (
    # urls for Teacher
    path('', views.TeacherListView.as_view(), name='initial_teacher_list'),
    path('login/',views.TeacherLoginView.as_view(), name="teacher_login"),
    path('logout/',views.TeacherLogoutView.as_view(), name='teacher_logout'),
    path('home_json/',views.Home_json.as_view(), name='home_json'),
    path('sections/',views.AssignedSections.as_view(), name='sections'),
    path('start_attendance/',views.StartSectionAttendance.as_view(), name = 'sections'),
    # path('create', views.TeacherCreateView.as_view(), name='initial_teacher_create'),
    # path('detail/<int:pk>/', views.TeacherDetailView.as_view(), name='initial_teacher_detail'),
    # path('update/<int:pk>/', views.TeacherUpdateView.as_view(), name='initial_teacher_update'),
)
