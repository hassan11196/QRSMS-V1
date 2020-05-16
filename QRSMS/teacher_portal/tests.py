from django.test import TestCase
from actor.models import User
from .models import Teacher
# Create your tests here
#


def create_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults['hassan'] = "hassan"

    defaults.update(**kwargs)
    user = User.objects.create(**defaults)
    user.set_password(user.password)
    user.save()
    return user


class TeacherTestCase(TestCase):
    def setUp(self):
        t1 = {
            "department": "Computer Sciences",
            "nu_email": "farrukh.hassan@nu.edu.pk",
            "user": create_user(username='farrukh.hassan').pk,
        }
        teacher_number_1 = Teacher.objects.create(**t1)

    def test_teachers_created(self):
        """Check if Teacher is created"""

        self.assertEqual(teacher_number_1.nu_email, 'farrukh.hassan@nu.edu.pk')
