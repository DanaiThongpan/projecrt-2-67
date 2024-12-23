# Generated by Django 5.0.3 on 2024-08-23 05:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_remove_user_is_recruitment_announcer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_person_responsible_for_the_project',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='user',
            name='number_of_credits_available',
        ),
        migrations.RemoveField(
            model_name='user',
            name='number_of_credits_required',
        ),
        migrations.RemoveField(
            model_name='user',
            name='type_Scholarship_or_Student_loan_fund',
        ),
        migrations.RemoveField(
            model_name='userperson_responsible_for_the_project',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userperson_responsible_for_the_project',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='userperson_responsible_for_the_project',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userperson_responsible_for_the_project',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='userperson_responsible_for_the_project',
            name='title',
        ),
        migrations.RemoveField(
            model_name='userstudent',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userstudent',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='userstudent',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userstudent',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='userstudent',
            name='title',
        ),
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(choices=[('นาย', 'นาย'), ('นางสาว', 'นางสาว'), ('นาง', 'นาง')], default='นาย', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='userperson_responsible_for_the_project',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='person_responsible_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userstudent',
            name='number_of_credits_available',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userstudent',
            name='number_of_credits_required',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userstudent',
            name='type_Scholarship_or_Student_loan_fund',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userstudent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
