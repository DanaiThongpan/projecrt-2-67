# Generated by Django 5.1.3 on 2024-12-24 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ActivityParticipationManagementSystem', '0008_db_create_activity_announcement_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_create_activity',
            name='semester',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
