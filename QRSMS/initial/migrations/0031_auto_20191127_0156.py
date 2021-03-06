# Generated by Django 2.2.7 on 2019-11-26 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_portal', '0006_auto_20191123_0907'),
        ('initial', '0030_auto_20191127_0124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfosection',
            name='attendance_sheet',
        ),
        migrations.AddField(
            model_name='studentinfosection',
            name='attendance_sheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='initial.AttendanceSheet'),
        ),
        migrations.RemoveField(
            model_name='studentinfosection',
            name='mark_sheet',
        ),
        migrations.AddField(
            model_name='studentinfosection',
            name='mark_sheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='initial.MarkSheet'),
        ),
        migrations.RemoveField(
            model_name='studentinfosection',
            name='student',
        ),
        migrations.AddField(
            model_name='studentinfosection',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_portal.Student'),
        ),
    ]
