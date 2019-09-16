# Generated by Django 2.2.5 on 2019-09-16 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('campus_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Campus ID')),
                ('Address', models.CharField(help_text='Address of Campus', max_length=255)),
                ('campus_name', models.CharField(help_text='Name of Campus of University', max_length=255)),
                ('campus_city', models.CharField(help_text='City Name of Campus', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Campuses',
            },
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.CharField(help_text='Education Level E.g: Bachelors, Masters, PhD', max_length=255, verbose_name='Education Level')),
                ('degree_name', models.CharField(help_text='Name Of Degree E.g: Computer Science(CS)', max_length=255, verbose_name='Degree Name')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('uni_id', models.AutoField(primary_key=True, serialize=False, verbose_name='University Registration ID')),
                ('name', models.CharField(help_text='Name of Univeristy', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'University',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_id', models.PositiveIntegerField(help_text='Department ID', verbose_name='Department ID')),
                ('departemnt_name', models.CharField(max_length=255, verbose_name='Department Name')),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Campuses_Department', to='institution.Campus')),
            ],
        ),
        migrations.AddField(
            model_name='campus',
            name='uni_name',
            field=models.ForeignKey(help_text='A university can have many campuses', on_delete=django.db.models.deletion.CASCADE, to='institution.University', verbose_name='Universities Campus'),
        ),
    ]
