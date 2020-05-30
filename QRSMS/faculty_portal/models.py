from django.db import models
from django.core.validators import RegexValidator, ValidationError
from django.urls import reverse
from actor.models import User
from django.contrib.auth.models import Group
# Create your models here.


class Faculty(models.Model):
    user = models.OneToOneField('actor.User', on_delete=models.CASCADE)

    @classmethod
    def create(cls, user=None, **kwargs):
        if user is None:
            username = None
            password = None

            username = kwargs['username']
            password = kwargs['password']

            u = User.create(username=kwargs['username'], password=kwargs['password'],
                            is_faculty=True, is_employee=True)
            user = u

        t = cls(user=user)
        t.save()
        # t.groups.add(Group.objects.get(name='faculty_group'))
        return t

    class Meta:
        ordering = ('-pk',)
        verbose_name_plural = "Faculty Supervisors"

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('initial_faculty_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('initial_faculty_update', args=(self.pk,))
