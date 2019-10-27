from django.core.validators import RegexValidator

UNIVERSITY_NAME = "FAST NUCES"
UNIVERSITY_FULL_NAME = "National University Of Computing And Emerging Sciences"
FOUNDATION_NAME = "Foundation for Advancement of Science And Technology"

CAMPUSES_CHOICES = (
    ('Karachi', 'K'),
    ('Lahore', 'L'),
    ('Faisalabad', 'F'),
    ('Islamabad', 'I'),
    ('Chiniot', 'C'),
    ('Peshawar', 'P')
)

CAMPUS_CHOICES_REGEX_STRING = "".join(map(lambda c: c[1], CAMPUSES_CHOICES))
UNIVERISTY_ID_REGEX = RegexValidator(
    "[0-9]{2}[" + CAMPUS_CHOICES_REGEX_STRING + "]-[0-9]{4}", message="INVALID ROLL NUMBER FORMAT")