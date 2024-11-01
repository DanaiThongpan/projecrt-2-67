from django.db import models, transaction
from Accounts.models import UserStudent, UserPerson_responsible_for_the_project, User
from django.core.exceptions import ValidationError
from django.utils import timezone  # สำหรับเช็คเวลาปัจจุบัน

# สร้าง Manager สำหรับปิดรับสมัครอัตโนมัติ
class ActivityManager(models.Manager):
    def close_expired_registrations(self):
        # ค้นหากิจกรรมที่วันปิดรับสมัครสิ้นสุดแล้ว และยังไม่ได้ปิดรับสมัคร
        expired_activities = self.filter(due_date_registration__lt=timezone.now(), is_registration_open=True)
        for activity in expired_activities:
            activity.is_registration_open = False
            activity.save()

class db_create_activity(models.Model):
    user = models.ForeignKey(UserPerson_responsible_for_the_project, on_delete=models.CASCADE, related_name='create_activity2')
    img_activity = models.ImageField(upload_to='activity/', blank=True, null=True)
    activity_name = models.CharField(max_length=30)
    activity_type = models.CharField(max_length=100, choices=[
        ('1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์', '1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์'),
        ('2 ด้านกีฬาหรือการส่งเสริมสุขภาพ', '2 ด้านกีฬาหรือการส่งเสริมสุขภาพ'),
        ('3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม', '3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม'),
        ('4 ด้านเสริมสร้างคุณธรรมและจริยธรรม', '4 ด้านเสริมสร้างคุณธรรมและจริยธรรม'),
        ('5 ด้านส่งเสริมศิลปะและวัฒนธรรม', '5 ด้านส่งเสริมศิลปะและวัฒนธรรม'),
        ('6 ด้านกิจกรรมอื่นๆ', '6 ด้านกิจกรรมอื่นๆ'),
    ])
    due_date_registration = models.DateTimeField()  # ฟิลด์ใหม่สำหรับวันปิดรับสมัคร
    place = models.CharField(max_length=30)
    start_date_activity = models.DateTimeField()
    due_date_activity = models.DateTimeField()
    description = models.CharField(max_length=30)
    credit = models.IntegerField(default=0)
    max_participants = models.IntegerField()
    registered_count = models.IntegerField(default=0)
    is_registration_open = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)  # เพิ่มฟิลด์นี้เพื่อเก็บค่าสถานะอนุมัติ
    
    # ผูก Manager ใหม่เข้ากับโมเดล
    objects = ActivityManager()

    def save(self, *args, **kwargs):
        # ตรวจสอบว่าปิดการรับสมัครหรือยัง
        if self.registered_count >= self.max_participants or timezone.now() > self.due_date_registration:
            self.is_registration_open = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} {self.img_activity} {self.activity_name} {self.activity_type} {self.place} {self.start_date_activity} {self.due_date_activity} {self.start_date_activity} {self.description}'

class ActivityPDF(models.Model):
    activity = models.ForeignKey(db_create_activity, on_delete=models.CASCADE, related_name='pdf_files')
    pdf_file = models.FileField(upload_to='activity_pdfs/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PDF for {self.activity.activity_name}'
    
from django.core.exceptions import PermissionDenied

class db_activity_adduser(models.Model):
    student = models.ForeignKey(User and UserStudent, on_delete=models.CASCADE, related_name='db_activity_adduser2')
    activity = models.ForeignKey(db_create_activity, on_delete=models.CASCADE, related_name='db_activity_adduser2')
    registered_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # ฟิลด์เพื่อเก็บสถานะการอนุมัติหน่วยกิต