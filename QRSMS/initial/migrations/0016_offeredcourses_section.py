# Generated by Django 2.2.7 on 2019-11-22 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0015_regularelectivecourseload_student_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='offeredcourses',
            name='section',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
