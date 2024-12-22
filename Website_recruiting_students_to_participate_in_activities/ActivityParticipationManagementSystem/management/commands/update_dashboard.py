from django.core.management.base import BaseCommand
from ActivityParticipationManagementSystem.models import db_create_activity, db_activity_adduser

class Command(BaseCommand):
    help = "อัปเดต registered_count ของกิจกรรมให้ตรงกับจำนวนนักศึกษาที่ลงทะเบียน"

    def handle(self, *args, **kwargs):
        # ดึงกิจกรรมทั้งหมด
        activities = db_create_activity.objects.all()

        for activity in activities:
            # นับจำนวนนักศึกษาที่ลงทะเบียนในกิจกรรมนี้
            registered_count = db_activity_adduser.objects.filter(activity=activity).count()

            # อัปเดตฟิลด์ registered_count
            activity.registered_count = registered_count
            activity.save()

            self.stdout.write(self.style.SUCCESS(f"อัปเดต registered_count ของกิจกรรม '{activity.activity_name}' เป็น {registered_count} คน"))

        self.stdout.write(self.style.SUCCESS("อัปเดต registered_count สำเร็จสำหรับทุกกิจกรรม!"))
