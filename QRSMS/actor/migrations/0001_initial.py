# Generated by Django 2.2.6 on 2019-10-25 14:59

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='username')),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE'), ('U', 'UNDEFINED'), ('O', 'OTHER')], max_length=50, verbose_name='Gender')),
                ('is_teacher', models.BooleanField(default=False, help_text='True if the User is a Teacher.')),
                ('is_student', models.BooleanField(default=False, help_text='True if the User is a Student.')),
                ('is_faculty', models.BooleanField(default=False, help_text='True if the User is a Faculty Member.')),
                ('is_maintainer', models.BooleanField(default=False, help_text='True if the User is a Mainatiner or Project Developer.')),
                ('CNIC', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('[0-9]{5}-[0-9]{7}-[0-9]{1}', message='Invalid CNIC')])),
                ('permanent_address', models.TextField(null=True)),
                ('permanent_home_phone', models.PositiveIntegerField(null=True)),
                ('permanent_postal_code', models.PositiveIntegerField(null=True)),
                ('permanent_city', models.TextField(max_length=100, null=True)),
                ('permanent_country', models.TextField(max_length=100, null=True)),
                ('current_address', models.TextField(null=True)),
                ('current_home_phone', models.PositiveIntegerField(null=True)),
                ('current_postal_code', models.PositiveIntegerField(null=True)),
                ('current_city', models.TextField(max_length=100, null=True)),
                ('current_country', models.TextField(max_length=100, null=True)),
                ('DOB', models.DateField(null=True, verbose_name='Date of Birth')),
                ('nationality', models.CharField(max_length=100, null=True, verbose_name='Nationality')),
                ('mobile_contact', models.PositiveIntegerField(null=True, verbose_name='Mobile Contact')),
                ('emergency_contact', models.PositiveIntegerField(null=True, verbose_name='Emergency Contact')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]