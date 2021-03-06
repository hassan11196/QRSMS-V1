from django.db import models
from django.shortcuts import reverse
from actor.models import User
from django.contrib.auth.models import Group
from institution.constants import DEFAULT_PASSWORD
# Create your models here.

QUALIFICATIONS = (
    (1, 'Bachelors'),
    (2, 'Masters'),
    (3, 'Doctrate')
)


class Teacher(models.Model):
    user = models.OneToOneField(
        'actor.User', on_delete=models.CASCADE, default=None)
    highest_qualification = models.SmallIntegerField(
        choices=QUALIFICATIONS, name='highest_qualification', null=True)
    # department = models.CharField(max_length=10, null=True)
    nu_email = models.CharField(max_length=100)

    @classmethod
    def create(cls, user=None, nu_email=None, **kwargs):
        if user is None:
            username = None
            password = None

            username = kwargs['username']
            password = kwargs['password']

            u = User.create(username=username, password=password,
                            is_teacher=True, is_employee=True)
            user = u

        t = cls(user=user, nu_email=nu_email)
        t.save()
        # t.groups.add(Group.objects.get(name='teacher_group'))
        return t

    # def save(self, *args, **kwargs):
    #     created = self.id is None
    #     super(YourModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk
