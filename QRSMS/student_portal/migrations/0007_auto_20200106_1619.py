# Generated by Django 2.2.7 on 2020-01-06 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_portal', '0006_auto_20191123_0907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('user',)},
        ),
    ]
