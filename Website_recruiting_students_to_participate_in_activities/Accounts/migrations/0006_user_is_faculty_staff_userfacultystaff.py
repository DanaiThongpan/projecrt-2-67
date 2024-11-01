# Generated by Django 5.0.3 on 2024-09-02 22:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_faculty_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='UserFacultyStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('นาย', 'นาย'), ('นางสาว', 'นางสาว'), ('นาง', 'นาง')], default='นาย', max_length=10)),
                ('faculty', models.CharField(choices=[('วิทยาศาสตร์', 'วิทยาศาสตร์'), ('คณะเกษตรศาสตร์', 'คณะเกษตรศาสตร์'), ('คณะวิศวกรรมศาสตร์', 'คณะวิศวกรรมศาสตร์'), ('คณะศิลปศาสตร์', 'คณะศิลปศาสตร์'), ('คณะเภสัชศาสตร์', 'คณะเภสัชศาสตร์'), ('คณะบริหารศาสตร์', 'คณะบริหารศาสตร์'), ('วิทยาลัยแพทยศาสตร์และการสาธารณสุข', 'วิทยาลัยแพทยศาสตร์และการสาธารณสุข'), ('คณะนิติศาสตร์', 'คณะนิติศาสตร์'), ('คณะรัฐศาสตร์', 'คณะรัฐศาสตร์'), ('คณะพยาบาลศาสตร์', 'คณะพยาบาลศาสตร์')], default='วิทยาศาสตร์', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facultystaff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
