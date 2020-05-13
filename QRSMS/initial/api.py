from . import models
from . import serializers
import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, routers
from rest_framework.response import Response


class StudentAttendanceViewSet(viewsets.ModelViewSet):
    queryset = models.StudentAttendance.objects.all()
    serializer_class = serializers.StudentAttendanceSerializerMinimized
    permission_classes = [permissions.IsAuthenticated, ]


class StudentInfoSectionViewSet(viewsets.ModelViewSet):
    queryset = models.StudentInfoSection.objects.all()
    serializer_class = serializers.StudentInfoSectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SectionAttendanceViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = models.SectionAttendance.objects.all()
    serializer_class = serializers.SectionAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = '__all__'


class AssignedSectionsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        print(user)
        return models.CourseSection.objects.filter(
            teacher__user__username=str(user)).all()
    # queryset = models.CourseSection.objects.all()
    serializer_class = serializers.CourseSectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AssignedSectionsAttendanceViewSet(viewsets.ViewSet):
    def list(self, request):
        course_section = models.CourseSection.objects.filter(
            teacher__user__username=str(request.user))
        data = []
        for x in course_section:
            print(x.scsddc)
            temp = {
                'section': serializers.CourseSectionSerializer(x, context={'request': self.request}).data,
                'section_attendance': serializers.CourseSectionSerializer(models.SectionAttendance.objects.filter(scsddc=x.scsddc).all(), context={'request': self.request}, many=True).data
            }
            data.append(temp)

        # models.SectionAttendance.objects.models.CourseSection.objects.filter(
        #         teacher__user__username=str(user)).filter(scsddc__in=.values_list('scsddc')).all()
        # SectionAttendance.objects.filter(scsddc__in=CourseSection.objects.filter(teacher__user__username=str('Abdul.Rehman')).values_list('scsddc')).all()
        return Response(data)

    # def get_queryset(self):
    #     user = self.request.user
    #     print(user)

    #     course_section = models.CourseSection.objects.filter(teacher__user__username=str(user))
    #     data = []
    #     for x in course_section:
    #         print(x.scsddc)
    #         temp = {
    #             'section':serializers.CourseSectionSerializer(x, context = {'request' : self.request}).data,
    #             'section_attendance':serializers.CourseSectionSerializer(models.SectionAttendance.objects.filter(scsddc=x.scsddc).all(), context  =  {'request' : self.request}, many = True).data
    #         }
    #         data.append(temp)

    #     # models.SectionAttendance.objects.models.CourseSection.objects.filter(
    #     #         teacher__user__username=str(user)).filter(scsddc__in=.values_list('scsddc')).all()
    #     # SectionAttendance.objects.filter(scsddc__in=CourseSection.objects.filter(teacher__user__username=str('Abdul.Rehman')).values_list('scsddc')).all()
    #     return data

    # # queryset = models.CourseSection.objects.all()
    # serializer_class = serializers.AssignedSectionAttendanceSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CourseSectionViewSet(viewsets.ModelViewSet):

    queryset = models.CourseSection.objects.all()
    serializer_class = serializers.CourseSectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = '__all__'


class MarkSheetViewSet(viewsets.ModelViewSet):
    queryset = models.MarkSheet.objects.all()
    serializer_class = serializers.MarkSheetSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceSheetViewSet(viewsets.ModelViewSet):
    queryset = models.AttendanceSheet.objects.all()
    serializer_class = serializers.AttendanceSheetSerializer
    permission_classes = [permissions.IsAuthenticated]


class OfferedCoursesViewSet(viewsets.ModelViewSet):
    queryset = models.OfferedCourses.objects.all()
    serializer_class = serializers.OfferedCoursesSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseStatusViewSet(viewsets.ModelViewSet):
    queryset = models.CourseStatus.objects.all()
    serializer_class = serializers.CourseStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSetDebug(viewsets.ModelViewSet):
    """ViewSet for the Course class"""

    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializerDebug
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for the Course class"""

    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    """ViewSet for the Teacher class"""

    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]


class FacultyViewSet(viewsets.ModelViewSet):
    """ViewSet for the Faculty class"""

    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Student class"""

    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SemesterViewSet(viewsets.ModelViewSet):
    """ViewSet for the Semester class"""

    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [permissions.IsAuthenticated]
