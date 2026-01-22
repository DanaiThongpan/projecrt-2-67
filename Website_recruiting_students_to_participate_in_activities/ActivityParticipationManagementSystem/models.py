from datetime import timedelta
from django.db import models, transaction
from Accounts.models import *
from django.core.exceptions import ValidationError
from django.utils import timezone  # สำหรับเช็คเวลาปัจจุบัน
from django.utils.timezone import now  # ใช้เพื่อดึงปีปัจจุบัน

# สร้าง Manager สำหรับปิดรับสมัครอัตโนมัติ
class ActivityManager(models.Manager):
    def close_expired_registrations(self):
        # ค้นหากิจกรรมที่วันปิดรับสมัครสิ้นสุดแล้ว และยังไม่ได้ปิดรับสมัคร
        expired_activities = self.filter(due_date_registration__lt=timezone.now(), is_registration_open=True)
        for activity in expired_activities:
            activity.is_registration_open = False
            activity.save()

# ฟังก์ชันกำหนดเส้นทางการจัดเก็บไฟล์ PDF แบบไดนามิก
def upload_to_activity_img_activity(instance, filename):
    """
    สร้างโฟลเดอร์สำหรับการจัดเก็บไฟล์ PDF โดยแยกตาม:
    - ชื่อคณะ (faculty)
    - ชื่อผู้ใช้ (username)
    """
    # ตรวจสอบและดึงข้อมูลจากผู้ใช้ที่เกี่ยวข้อง
    if instance.user_faculty_staff:
        user_type = 'faculty_staff'
        faculty = instance.user_faculty_staff.faculty
        user_create = instance.user_faculty_staff.user.first_name
    elif instance.user_person_responsible:
        user_type = 'person_responsible'
        faculty = instance.user_person_responsible.faculty
        user_create = instance.user_person_responsible.user.first_name
    else:
        user_type = 'unknown_user'
        faculty = 'unknown_faculty'
        user_create = 'unknown_user'

    # กำหนดโฟลเดอร์เก็บไฟล์
    #แก้ชื่อ activity_pdfs
    return os.path.join(f'activity_pdfs/{user_type}/{faculty}/{user_create}/{instance.activity_name}', filename)

act_choices=[
        ('1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์', '1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์'),
        ('2 ด้านกีฬาหรือการส่งเสริมสุขภาพ', '2 ด้านกีฬาหรือการส่งเสริมสุขภาพ'),
        ('3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม', '3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม'),
        ('4 ด้านเสริมสร้างคุณธรรมและจริยธรรม', '4 ด้านเสริมสร้างคุณธรรมและจริยธรรม'),
        ('5 ด้านส่งเสริมศิลปะและวัฒนธรรม', '5 ด้านส่งเสริมศิลปะและวัฒนธรรม'),
        ('6 ด้านกิจกรรมอื่นๆ', '6 ด้านกิจกรรมอื่นๆ'),
    ]

class db_create_activity(models.Model):
    user_faculty_staff = models.ForeignKey(UserFacultyStaff, null=True, blank=True, on_delete=models.CASCADE, related_name='create_activity_faculty')
    user_person_responsible = models.ForeignKey(UserPerson_responsible_for_the_project, null=True, blank=True, on_delete=models.CASCADE, related_name='create_activity_responsible')
    img_activity = models.ImageField(upload_to=upload_to_activity_img_activity, blank=True, null=True)
    activity_name = models.CharField(max_length=30)
    activity_type = models.CharField(max_length=100, choices=act_choices)
    due_date_registration = models.DateTimeField()  # ฟิลด์ใหม่สำหรับวันปิดรับสมัคร
    description = models.CharField(max_length=30)
    credit = models.IntegerField(default=0)
    max_participants = models.IntegerField()
    registered_count = models.IntegerField(default=0)
    is_registration_open = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)  # เพิ่มฟิลด์นี้เพื่อเก็บค่าสถานะอนุมัติ
    # current_year = now().year + 543

    # SEMESTER_CHOICES = [
    #     (f'1/{current_year}', f'1/{current_year}'),
    #     (f'2/{current_year}', f'2/{current_year}'),
    # ]

    announcement_date = models.DateTimeField(auto_now_add=True)  # วันที่ประกาศ (ตั้งค่าอัตโนมัติ)
    # semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, blank=True)  # ภาคการศึกษา

    number_of_days = models.IntegerField(default=1)  # จำนวนวันที่จัดกิจกรรม (เริ่มต้นที่ 1)


    # แยกเทอมและปีการศึกษา
    SEMESTER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
    ]
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, blank=True)

    academic_year = models.IntegerField(default=now().year + 543)  # ปีการศึกษาแบบ พ.ศ.

    objects = ActivityManager()

    def save(self, *args, **kwargs):
        current_year = now().year + 543
        SEMESTER_CHOICES = [
            (f'1', f'1'),
            (f'2', f'2'),
        ]
        self._meta.get_field('semester').choices = SEMESTER_CHOICES

        if not self.semester:
            self.semester = f'1/{current_year}'

        if self.registered_count >= self.max_participants or timezone.now() > self.due_date_registration:
            self.is_registration_open = False
        super().save(*args, **kwargs)

class TimeEvent(models.Model):
    activity_id = models.ForeignKey(db_create_activity, null=True, blank=True, on_delete=models.CASCADE, related_name='TimeEvent')
    place = models.CharField(max_length=30)
    start_date_activity = models.DateTimeField()
    due_date_activity = models.DateTimeField()

import os

# ฟังก์ชันกำหนดเส้นทางการจัดเก็บไฟล์ PDF แบบไดนามิก
def upload_to_activity_pdfs(instance, filename):
    """
    สร้างโฟลเดอร์สำหรับการจัดเก็บไฟล์ PDF โดยแยกตาม:
    - ชื่อคณะ (faculty)
    - ชื่อผู้ใช้ (username)
    """
    user = instance.activity

    # ตรวจสอบสถานะผู้ใช้และกำหนดชื่อโฟลเดอร์
    if user.user_faculty_staff:
        user_type = 'faculty_staff'
        faculty = user.user_faculty_staff.faculty
        user_create = user.user_faculty_staff.user.first_name
    elif user.user_person_responsible:
        user_type = 'person_responsible'
        faculty = user.user_person_responsible.faculty
        user_create = user.user_person_responsible.user.first_name
    else:
        user_type = 'unknown_user'

    # ใช้ชื่อคณะเป็นชื่อโฟลเดอร์
    #แก้ชื่อ activity_pdfs
    return os.path.join(f'activity_pdfs/{user_type}/{faculty}/{user_create}/{user.activity_name}', filename)

# โมเดล ActivityPDF
class ActivityPDF(models.Model):
    activity = models.ForeignKey('db_create_activity', on_delete=models.CASCADE, related_name='pdf_files')
    pdf_file = models.FileField(upload_to=upload_to_activity_pdfs, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PDF for {self.activity.activity_name}'

    
from django.core.exceptions import PermissionDenied

class db_activity_adduser(models.Model):
    student = models.ForeignKey(User and UserStudent, on_delete=models.CASCADE, related_name='db_activity_adduser2')
    activity = models.ForeignKey(db_create_activity, on_delete=models.CASCADE, related_name='db_activity_adduser2')
    registered_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # ฟิลด์เพื่อเก็บสถานะการอนุมัติหน่วยกิต ตรวจรายชื่อ


