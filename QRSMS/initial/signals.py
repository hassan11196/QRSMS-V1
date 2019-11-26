from django.dispatch import Signal

attendance_sheet_for_student = Signal(providing_args=['student', 'course_section','option'])
mark_sheet_for_student = Signal(providing_args=['student', 'course_section','option'])
student_info_section_for_student = Signal(providing_args=['student', 'course_section','option'])