from django.db import models
from django.shortcuts import reverse
# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField('actor.User', on_delete=models.CASCADE, default=None)
    department = models.CharField(max_length=10)
    nu_email = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
        
    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('initial_teacher_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('initial_teacher_update', args=(self.pk,))
