# Generated by Django 2.2 on 2020-05-30 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0048_auto_20200527_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionmarks',
            name='marks_mean',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='sectionmarks',
            name='marks_standard_deviation',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='sectionmarks',
            name='weightage_mean',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='sectionmarks',
            name='weightage_standard_deviation',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='marksheet',
            name='grade',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
