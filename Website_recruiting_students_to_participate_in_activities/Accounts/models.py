from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

title__choices = [('นาย', 'นาย'), ('นางสาว', 'นางสาว'), ('นาง', 'นาง')]

faculty_choices = [ ('วิทยาศาสตร์', 'วิทยาศาสตร์'), ('คณะเกษตรศาสตร์', 'คณะเกษตรศาสตร์'), ('คณะวิศวกรรมศาสตร์', 'คณะวิศวกรรมศาสตร์'), ('คณะศิลปศาสตร์', 'คณะศิลปศาสตร์'), ('คณะเภสัชศาสตร์', 'คณะเภสัชศาสตร์'), ('คณะบริหารศาสตร์', 'คณะบริหารศาสตร์'), ('วิทยาลัยแพทยศาสตร์และการสาธารณสุข', 'วิทยาลัยแพทยศาสตร์และการสาธารณสุข'), ('คณะนิติศาสตร์', 'คณะนิติศาสตร์'), ('คณะรัฐศาสตร์', 'คณะรัฐศาสตร์'), ('คณะพยาบาลศาสตร์', 'คณะพยาบาลศาสตร์')]

type_Scholarship_or_Student_loan_fund__choices = [('ทุน', 'ทุน'),('กยศ', 'กยศ'),('ทุน, กยศ', 'ทุน, กยศ')]

#ผู้ใช้ทั้งหมด
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_person_responsible_for_the_project = models.BooleanField(default=False)
    is_faculty_staff = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return (f'{self.username, self.first_name, self.last_name }')
    
#นักเรียน
class UserStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentprofile')
    type_Scholarship_or_Student_loan_fund = models.CharField(max_length=50, choices=type_Scholarship_or_Student_loan_fund__choices)
    number_of_credits_required = models.IntegerField()
    number_of_credits_available = models.IntegerField()
    title = models.CharField(max_length=10, choices=title__choices, default="นาย")
    faculty = models.CharField(max_length=50, choices=faculty_choices, default="วิทยาศาสตร์")

    def __str__(self) -> str:
        return (f'{self.user, self.faculty, self.title }')
    
#ผู้รับผิดชอบโครงการ
class UserPerson_responsible_for_the_project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_responsible_for_the_projectprofile')
    title = models.CharField(max_length=10, choices=title__choices, default="นาย")
    faculty = models.CharField(max_length=50, choices=faculty_choices, default="วิทยาศาสตร์")
 
    def __str__(self) -> str:
        return (f'{self.user, self.faculty, self.title }')

#เจ้าหน้าที่คณะ
class UserFacultyStaff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facultystaff')
    title = models.CharField(max_length=10, choices=title__choices, default="นาย")
    faculty = models.CharField(max_length=50, choices=faculty_choices, default="วิทยาศาสตร์")
    is_approved = models.BooleanField(default=False)  # เพิ่มฟิลด์นี้เพื่อเก็บค่าสถานะอนุมัติ

    def __str__(self) -> str:
        return (f'{self.user, self.faculty, self.title }')
    