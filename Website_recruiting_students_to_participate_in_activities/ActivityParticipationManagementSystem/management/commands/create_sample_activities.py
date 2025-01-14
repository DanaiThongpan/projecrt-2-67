from django.core.management.base import BaseCommand
from ActivityParticipationManagementSystem.models import db_create_activity, UserFacultyStaff, UserPerson_responsible_for_the_project
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'สร้างข้อมูลกิจกรรมตัวอย่างตามประเภทกิจกรรม'

    def handle(self, *args, **kwargs):
        # กำหนดข้อมูลที่ใช้
        faculty_staff = UserFacultyStaff.objects.all()
        responsible_staff = UserPerson_responsible_for_the_project.objects.all()

        # ประเภทกิจกรรม
        activity_types = [
            '1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์',
            '2 ด้านกีฬาหรือการส่งเสริมสุขภาพ',
            '3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม',
            '4 ด้านเสริมสร้างคุณธรรมและจริยธรรม',
            '5 ด้านส่งเสริมศิลปะและวัฒนธรรม',
            '6 ด้านกิจกรรมอื่นๆ',
        ]

        # จำนวนกิจกรรมในแต่ละประเภท (3-5 กิจกรรม)
        activities_per_type = random.randint(3, 5)

        # ข้อมูลกิจกรรมตัวอย่าง
        for activity_type in activity_types:
            for _ in range(activities_per_type):
                # สุ่มเลือก user_faculty_staff และ user_person_responsible สำหรับการกำหนด
                user_faculty_staff = random.choice(faculty_staff)
                user_person_responsible = random.choice(responsible_staff)
                
                # สร้างข้อมูลกิจกรรมใหม่
                activity = db_create_activity(
                    user_faculty_staff=user_faculty_staff,
                    user_person_responsible=user_person_responsible,
                    activity_name=f'{activity_type} {random.randint(1, 100)}',  # สร้างชื่อกิจกรรม
                    activity_type=activity_type,
                    due_date_registration=timezone.now() + timedelta(days=random.randint(10, 30)),
                    place=f'สถานที่ {random.randint(1, 10)}',
                    start_date_activity=timezone.now() + timedelta(days=random.randint(1, 7)),
                    due_date_activity=timezone.now() + timedelta(days=random.randint(10, 30)),
                    description=f'คำอธิบายกิจกรรม {activity_type}',
                    credit=random.randint(1, 5),
                    max_participants=random.randint(20, 100),
                    registered_count=0,
                    is_approved=False,
                    semester=f'1/{timezone.now().year + 543}',
                )
                
                activity.save()
                self.stdout.write(self.style.SUCCESS(f'กิจกรรม "{activity.activity_name}" ถูกเพิ่มแล้ว!'))
