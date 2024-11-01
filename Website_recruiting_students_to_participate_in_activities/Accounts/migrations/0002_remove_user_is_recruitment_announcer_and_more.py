# Generated by Django 5.0.3 on 2024-08-23 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_recruitment_announcer',
        ),
        migrations.RemoveField(
            model_name='userperson_responsible_for_the_project',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='userperson_responsible_for_the_project',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='userstudent',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='userstudent',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='user',
            name='number_of_credits_available',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='number_of_credits_required',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='type_Scholarship_or_Student_loan_fund',
            field=models.CharField(choices=[('ทุน', 'ทุน'), ('กยศ', 'กยศ'), ('ทุน, กยศ', 'ทุน, กยศ')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstudent',
            name='number_of_credits_available',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstudent',
            name='number_of_credits_required',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstudent',
            name='type_Scholarship_or_Student_loan_fund',
            field=models.CharField(choices=[('ทุน', 'ทุน'), ('กยศ', 'กยศ'), ('ทุน, กยศ', 'ทุน, กยศ')], default=11, max_length=50),
            preserve_default=False,
        ),
    ]
