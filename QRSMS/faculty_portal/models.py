from django.db import models
from django.core.validators import RegexValidator, ValidationError
from django.urls import reverse

# Create your models here.


class Faculty(models.Model):
    user = models.OneToOneField('actor.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)
        verbose_name_plural = "Faculty Supervisors"

    def get_absolute_url(self):
        return reverse('initial_faculty_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('initial_faculty_update', args=(self.pk,))