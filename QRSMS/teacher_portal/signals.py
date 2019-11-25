from django.dispatch import Signal

attendance_of_day_for_student = Signal(providing_args=['coursesection','scsddc', 'slot','option'])