# Generated by Django 2.2.7 on 2019-11-15 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_portal', '0003_student_admission_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='admission_section',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
