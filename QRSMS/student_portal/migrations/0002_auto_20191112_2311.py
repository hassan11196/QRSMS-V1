# Generated by Django 2.2.7 on 2019-11-12 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='current_semester',
            field=models.PositiveSmallIntegerField(help_text='Number of semester the student is Attending.', null=True),
        ),
    ]