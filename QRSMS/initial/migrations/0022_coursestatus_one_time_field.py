# Generated by Django 2.2.7 on 2019-11-23 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0021_remove_coursestatus_one_time_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursestatus',
            name='one_time_field',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]