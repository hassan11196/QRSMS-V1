# Generated by Django 2.2.7 on 2019-11-23 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0019_coursestatus_one_time_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursestatus',
            name='one_time_field',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
