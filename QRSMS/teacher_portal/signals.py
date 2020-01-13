from django.dispatch import Signal

attendance_of_day_for_student = Signal(providing_args=['scsddc','coursesection','sectionattendance','option'])
marks_for_student = Signal(providing_args=['scsddc','coursesection','sectionmarks','option'])