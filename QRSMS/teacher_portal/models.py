from django.db import models
from django.shortcuts import reverse
# Create your models here.

QUALIFICATIONS = (
    (1, 'Bachelors'),
    (2 , 'Masters'),
    (3 ,'Doctrate')
)

class Teacher(models.Model):
    user = models.OneToOneField('actor.User', on_delete=models.CASCADE, default=None)
    highest_qualification = models.SmallIntegerField(choices=QUALIFICATIONS,name='highest_qualification', null=True)
    # department = models.CharField(max_length=10, null=True)
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
