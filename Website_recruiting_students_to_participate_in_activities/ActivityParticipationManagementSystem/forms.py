from django import forms
# from django.db import models
# from Accounts.forms import UserStudentrRegistrationForm
from Accounts.models import User, UserPerson_responsible_for_the_project
# from django.contrib.auth.forms import UserChangeForm

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
            'due_date_registration',
            'max_participants',
            # 'place',
            # 'start_date_activity',
            # 'due_date_activity',
            'description',
            'credit',
            'number_of_days',
        ]

        labels = {
            'img_activity' : 'รูปกิจกรรม ',
            'activity_name' : 'ชื่อกิจกรรม ',
            'activity_type' : 'ด้านที่ ',
            'due_date_registration' : 'เปิดให้ลงทะเบียนถึงวันที่',
            # 'start_date_create_activity' : 'วันที่เปิดรับสมัคร ',
            # 'due_date_create_activity' : 'วันที่ปิดรับสมัคร ',
            'max_participants' : 'จำนวนเป้าหมาย ',
            # 'place' : 'สถานที่จัดกิจกรรม ',
            # 'start_date_activity' : 'วันที่จัดกิจกรรม ',
            # 'due_date_activity' : 'วันที่สิ้นสุดกิจกรรม ',
            'description' : 'คำอธิบาย ',
            'credit' : 'หน่วยกิจกรรม',
        }

        widgets = {
            # 'start_date_create_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            # 'due_date_create_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            # 'start_date_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            # 'due_date_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            'due_date_registration': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
        }

class TimeEvent_activity(forms.ModelForm):
    class Meta:
        model = TimeEvent
        fields = ['activity_id']  # ตัวอย่างฟิลด์ที่ต้องการ

        labels = {
            'activity_id' : 'id',
            'place' : 'สถานที่จัดกิจกรรม ',
            'start_date_activity' : 'วันที่จัดกิจกรรม ',
            'due_date_activity' : 'วันที่สิ้นสุดกิจกรรม ',
        }

        widgets = {
            'start_date_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
            'due_date_activity': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, num_of_days=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_of_days = num_of_days
        
        # ซ่อนฟิลด์ activity_id
        self.fields['activity_id'].widget = forms.HiddenInput()  # ซ่อน activity_id ในฟอร์ม

        # สร้างฟิลด์แบบไดนามิกตามจำนวนวันที่
        for i in range(self.num_of_days):
            self.fields[f'start_date_activity_{i}'] = forms.DateTimeField(
                label=f'วันที่เริ่มกิจกรรม (วันที่ {i+1})',
                required=True,
                widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'})
            )
            self.fields[f'due_date_activity_{i}'] = forms.DateTimeField(
                label=f'วันที่สิ้นสุดกิจกรรม (วันที่ {i+1})',
                required=True,
                widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'type': 'datetime-local'})
            )
            self.fields[f'place{i}'] = forms.CharField(
                label=f'สถานที่จัดกิจกรรม (วันที่ {i+1})',
                required=True
            )

from .models import db_activity_adduser

class forms_activity_adduser(forms.ModelForm):
    class Meta:
        model = db_activity_adduser
        fields = '__all__'

class ActivityPDFForm(forms.ModelForm):
    class Meta:
        model = ActivityPDF
        fields = ['pdf_file']