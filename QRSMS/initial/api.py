from . import models
from . import serializers
from rest_framework import viewsets, permissions, routers


class SectionAttendanceViewSet(viewsets.ModelViewSet):
    queryset = models.SectionAttendance.objects.all()
    serializer_class = serializers.SectionAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = models.CourseSection.objects.all()
    serializer_class = serializers.CourseSectionSerializer
    permission_classes = [permissions.IsAuthenticated]

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


