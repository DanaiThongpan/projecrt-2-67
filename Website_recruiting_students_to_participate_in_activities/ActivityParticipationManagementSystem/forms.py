from django import forms
# from django.db import models
# from Accounts.forms import UserStudentrRegistrationForm
from Accounts.models import User, UserPerson_responsible_for_the_project
from django.contrib.auth.forms import UserChangeForm

# Create your models here.
    
from ActivityParticipationManagementSystem.models import *

class forms_create_activity(forms.ModelForm):
    class Meta:
        model = db_create_activity
        fields = [
            'img_activity',
            # 'user_faculty_staff',
            # 'user_person_responsible',
            'semester',
            'activity_name',
            'activity_type',
            # 'start_date_create_activity',
            # 'due_date_create_activity',
            'due_date_registration',
            'max_participants',
            'place',
            'start_date_activity',
            'due_date_activity',
            'description',
            'credit',
        ]

        labels = {
            'img_activity' : 'รูปกิจกรรม ',
            'activity_name' : 'ชื่อกิจกรรม ',
            'activity_type' : 'ด้านที่ ',
            'due_date_registration' : 'เปิดให้ลงทะเบียนถึงวันที่',
            # 'start_date_create_activity' : 'วันที่เปิดรับสมัคร ',
            # 'due_date_create_activity' : 'วันที่ปิดรับสมัคร ',
            'max_participants' : 'จำนวนเป้าหมาย ',
            'place' : 'สถานที่จัดกิจกรรม ',
            'start_date_activity' : 'วันที่จัดกิจกรรม ',
            'due_date_activity' : 'วันที่สิ้นสุดกิจกรรม ',
            'description' : 'คำอธิบาย ',
            'credit' : 'หน่วยกิจกรรม',
        }

        widgets = {
            # 'start_date_create_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            # 'due_date_create_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            'start_date_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            'due_date_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            'due_date_registration': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
        }

from .models import db_activity_adduser

class forms_activity_adduser(forms.ModelForm):
    class Meta:
        model = db_activity_adduser
        fields = '__all__'

class ActivityPDFForm(forms.ModelForm):
    class Meta:
        model = ActivityPDF
        fields = ['pdf_file']