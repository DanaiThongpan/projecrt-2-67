import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from Accounts.models import User, UserStudent
from ActivityParticipationManagementSystem.models import db_activity_adduser, db_create_activity


class Command(BaseCommand):
    help = "สร้าง User, UserStudent และลงทะเบียนในกิจกรรม ID 1"

    def handle(self, *args, **kwargs):
        # ดึงกิจกรรมที่มี ID = 1
        try:
            activity = db_create_activity.objects.get(id=1)
        except db_create_activity.DoesNotExist:
            self.stdout.write(self.style.ERROR("กิจกรรม ID 1 ไม่พบในฐานข้อมูล"))
            return

        # สร้าง User และ UserStudent
        for i in range(1, 31):
            # สร้าง User
            user = User.objects.create_user(
                username=f'user{i}',
                first_name=f'FirstName{i}',
                last_name=f'LastName{i}',
                email=f'user{i}@example.com',
                password='testpassword'
            )
            user.is_student = True  # กำหนดสถานะเป็น Student
            user.save()

            # สร้าง UserStudent
            student_profile = UserStudent.objects.create(
                user=user,
                type_Scholarship_or_Student_loan_fund='ทุน',
                number_of_credits_required=random.randint(10, 20),
                number_of_credits_available=random.randint(5, 10),
                title='นาย',
                faculty='วิทยาศาสตร์'
            )

            # ลงทะเบียนในกิจกรรม
            db_activity_adduser.objects.create(
                student=student_profile,
                activity=activity,
                registered_at=datetime.now() - timedelta(days=random.randint(1, 10)),  # สุ่มวันที่ลงทะเบียน
                is_approved=random.choice([True, False])  # สุ่มสถานะอนุมัติ
            )

        self.stdout.write(self.style.SUCCESS("สร้าง User และลงทะเบียนกิจกรรมสำเร็จ!"))