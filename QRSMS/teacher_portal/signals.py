from django.dispatch import Signal, receiver

attendance_of_day_for_student = Signal(
    providing_args=['scsddc', 'coursesection', 'sectionattendance', 'option'])
marks_for_student = Signal(
    providing_args=['scsddc', 'coursesection', 'sectionmarks', 'option'])


@receiver(attendance_of_day_for_student)
def start_attendance_for_student(**kwargs):
    print(kwargs['scsddc'])
    print(kwargs['coursesection'])
    print(kwargs['sectionattendance'])
    print(kwargs['option'])
