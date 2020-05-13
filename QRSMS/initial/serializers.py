
from .models import Course, RegularCoreCourseLoad, RegularElectiveCourseLoad, OfferedCourses, CourseStatus, MarkSheet, AttendanceSheet, CourseSection, SectionAttendance, MarkSheet, StudentInfoSection, StudentAttendance, StudentMarks, SectionMarks
from rest_framework import serializers
from . import models
from student_portal.serializers import StudentSerializerOnlyNameAndUid, WrapperStudentSerializer


class StudentAttendanceSerializerMinimized(serializers.HyperlinkedModelSerializer):
    # attendance_sheet = serializers.PrimaryKeyRelatedField(many=True, queryset=models.AttendanceSheet.objects.all())
    class Meta:
        model = StudentAttendance
        fields = ('url', 'class_date', 'attendance_slot',
                  'state', 'duration_hour')


class StudentAttendanceSheetSerializerMinimized(serializers.HyperlinkedModelSerializer):
    attendance = StudentAttendanceSerializerMinimized(many=True)
    student = WrapperStudentSerializer('uid')

    class Meta:
        model = AttendanceSheet
        fields = ('url', 'student', 'scsddc', 'attendance',)


class StudentAttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'


class StudentInfoSectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StudentInfoSection
        fields = '__all__'


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseSerializerDebug(serializers.ModelSerializer):
    course_status_offer = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.CourseStatus.objects.all())

    class Meta:
        model = Course
        fields = ['course_code', 'course_name',
                  'course_type', 'course_status_offer']


class StudentInfoSectionModelSerializerGetAttendance(serializers.ModelSerializer):
    student = StudentSerializerOnlyNameAndUid()
    attendance_sheet = StudentAttendanceSheetSerializerMinimized()

    class Meta:
        model = StudentInfoSection
        fields = '__all__'


class SectionAttendanceSerializer(serializers.ModelSerializer):

    student_attendance_list = serializers.SerializerMethodField(
        'attendance_list')

    def attendance_list(self, section_att):
        sa = StudentAttendance.objects.filter(class_date=section_att.class_date, attendance_slot=section_att.attendance_slot,
                                              scsddc=section_att.scsddc)

        return StudentAttendanceSerializer(sa, many=True, context={'request': self.context['request']}).data

    class Meta:
        model = SectionAttendance
        fields = '__all__'


class AssignedSectionAttendanceSerializer(serializers.Serializer):

    section = SectionAttendanceSerializer(many=True)
    section_attendance = SectionAttendanceSerializer(many=True)

    # class Meta:
    #     fields = '__all__'
    #     model = dict


class SectionMarksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SectionMarks
        fields = '__all__'


class CourseSectionSerializer(serializers.HyperlinkedModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     # Don't pass the 'fields' arg up to the superclass
    #     fields = kwargs.pop('fields', None)
    #     # Instantiate the superclass normally
    #     super(CourseSectionSerializer, self).__init__(*args, **kwargs)

    #     for course in self.instance:
    #         course.course_name = Course.objects.get(course_code = course.course_code)

    class Meta:
        model = CourseSection
        fields = '__all__'
        depth = 1
    # course = CourseSerializer()


class StudentMarksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentMarks
        fields = '__all__'


class MarkSheetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarkSheet
        fields = '__all__'


class AttendanceSheetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AttendanceSheet
        fields = '__all__'
        depth = 1


class OfferedCoursesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferedCourses
        fields = ('courses_offered', 'semester_code')
        depth = 2


class CourseStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseStatus
        fields = '__all__'


class RegularCoreCourseLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularCoreCourseLoad
        fields = '__all__'
        depth = 1


class RegularElectiveCourseLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularElectiveCourseLoad
        fields = '__all__'
        depth = 3
# class StudentSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['arn','uid','user']


# class CourseSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.Course
#         fields = (
#             'pk',
#             'course_name',
#             'course_code',
#         )


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Teacher
        fields = (
            'pk',
            'department',
            'nu_email',
        )


class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Faculty
        fields = (
            'pk',
        )


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Student
        fields = (
            'pk',
            'batch',
            'arn',
            'uid',
            'degree_name_enrolled',
            'degree_short_enrolled',
            'department_name_enrolled',
            'uni_mail',
        )


class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Semester
        fields = [
            'semester_code',
            'semester_season', 'semester_year', 'start_date', 'end_date'
        ]
