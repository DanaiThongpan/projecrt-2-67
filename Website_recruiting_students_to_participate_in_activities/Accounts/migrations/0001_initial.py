# Generated by Django 5.0.3 on 2024-08-03 19:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_recruitment_announcer', models.BooleanField(default=False)),
                ('is_person_responsible_for_the_project', models.BooleanField(default=False)),
                ('faculty', models.CharField(choices=[('วิทยาศาสตร์', 'วิทยาศาสตร์'), ('คณะเกษตรศาสตร์', 'คณะเกษตรศาสตร์'), ('คณะวิศวกรรมศาสตร์', 'คณะวิศวกรรมศาสตร์'), ('คณะศิลปศาสตร์', 'คณะศิลปศาสตร์'), ('คณะเภสัชศาสตร์', 'คณะเภสัชศาสตร์'), ('คณะบริหารศาสตร์', 'คณะบริหารศาสตร์'), ('วิทยาลัยแพทยศาสตร์และการสาธารณสุข', 'วิทยาลัยแพทยศาสตร์และการสาธารณสุข'), ('คณะนิติศาสตร์', 'คณะนิติศาสตร์'), ('คณะรัฐศาสตร์', 'คณะรัฐศาสตร์'), ('คณะพยาบาลศาสตร์', 'คณะพยาบาลศาสตร์')], default='วิทยาศาสตร์', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
        migrations.CreateModel(
            name='UserStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(choices=[('นาย', 'นาย'), ('นางสาว', 'นางสาว'), ('นาง', 'นาง')], default='นาย', max_length=10)),
                ('faculty', models.CharField(choices=[('วิทยาศาสตร์', 'วิทยาศาสตร์'), ('คณะเกษตรศาสตร์', 'คณะเกษตรศาสตร์'), ('คณะวิศวกรรมศาสตร์', 'คณะวิศวกรรมศาสตร์'), ('คณะศิลปศาสตร์', 'คณะศิลปศาสตร์'), ('คณะเภสัชศาสตร์', 'คณะเภสัชศาสตร์'), ('คณะบริหารศาสตร์', 'คณะบริหารศาสตร์'), ('วิทยาลัยแพทยศาสตร์และการสาธารณสุข', 'วิทยาลัยแพทยศาสตร์และการสาธารณสุข'), ('คณะนิติศาสตร์', 'คณะนิติศาสตร์'), ('คณะรัฐศาสตร์', 'คณะรัฐศาสตร์'), ('คณะพยาบาลศาสตร์', 'คณะพยาบาลศาสตร์')], default='วิทยาศาสตร์', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_student_groups', to='auth.group', verbose_name='Groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_student_user_permissions', to='auth.permission', verbose_name='User Permissions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPerson_responsible_for_the_project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(choices=[('นาย', 'นาย'), ('นางสาว', 'นางสาว'), ('นาง', 'นาง')], default='นาย', max_length=10)),
                ('faculty', models.CharField(choices=[('วิทยาศาสตร์', 'วิทยาศาสตร์'), ('คณะเกษตรศาสตร์', 'คณะเกษตรศาสตร์'), ('คณะวิศวกรรมศาสตร์', 'คณะวิศวกรรมศาสตร์'), ('คณะศิลปศาสตร์', 'คณะศิลปศาสตร์'), ('คณะเภสัชศาสตร์', 'คณะเภสัชศาสตร์'), ('คณะบริหารศาสตร์', 'คณะบริหารศาสตร์'), ('วิทยาลัยแพทยศาสตร์และการสาธารณสุข', 'วิทยาลัยแพทยศาสตร์และการสาธารณสุข'), ('คณะนิติศาสตร์', 'คณะนิติศาสตร์'), ('คณะรัฐศาสตร์', 'คณะรัฐศาสตร์'), ('คณะพยาบาลศาสตร์', 'คณะพยาบาลศาสตร์')], default='วิทยาศาสตร์', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_person_responsible_for_the_project_groups', to='auth.group', verbose_name='Groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_person_responsible_for_the_project_user_permissions', to='auth.permission', verbose_name='User Permissions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_responsible_for_the_projectprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
