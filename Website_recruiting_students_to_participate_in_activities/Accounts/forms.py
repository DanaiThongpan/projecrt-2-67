from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Accounts.models import *

#ผู้ใช้ทั้งหมด
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'username': 'ชื่อผู้ใช้งาน','first_name': 'ชื่อ','last_name': 'นามสกุล','email': 'อีเมล'}

#นักเรียน
class UserStudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserStudent
        fields = ['title', 'faculty', 
                  'number_of_credits_required1',
                  'number_of_credits_available1', 
                  'number_of_credits_required2',
                  'number_of_credits_available2', 
                  'number_of_credits_required3',
                  'number_of_credits_available3', 
                  'number_of_credits_required4',
                  'number_of_credits_available4', 
                  'number_of_credits_required5',
                  'number_of_credits_available5', 
                  'number_of_credits_required6',
                  'number_of_credits_available6', 
                  'type_Scholarship_or_Student_loan_fund']
        labels = {'title' : 'คำนำหน้า', 
                  'faculty' : 'คณะ', 
                  'number_of_credits_required1' : 'หน่วยกิตที่ต้องการ 1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์', 
                  'number_of_credits_available1' : 'หน่วยกิตที่มี',
                  'number_of_credits_required2' : 'หน่วยกิตที่ต้องการ 2 ด้านกีฬาหรือการส่งเสริมสุขภาพ', 
                  'number_of_credits_available2' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required3' : 'หน่วยกิตที่ต้องการ 3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม', 
                  'number_of_credits_available3' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required4' : 'หน่วยกิตที่ต้องการ 4 ด้านเสริมสร้างคุณธรรมและจริยธรรม', 
                  'number_of_credits_available4' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required5' : 'หน่วยกิตที่ต้องการ 5 ด้านส่งเสริมศิลปะและวัฒนธรรม', 
                  'number_of_credits_available5' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required6' : 'หน่วยกิตที่ต้องการ 6 ด้านกิจกรรมอื่นๆ', 
                  'number_of_credits_available6' : 'หน่วยกิตที่มี', 
                  'type_Scholarship_or_Student_loan_fund' : 'ประเภท(ทุน-กยศ)'}
        
class UserStudentUpdateForm(forms.ModelForm):
    class Meta:
        model = UserStudent
        fields = ['title', 'faculty', 
                  'number_of_credits_required1',
                  'number_of_credits_available1', 
                  'number_of_credits_required2',
                  'number_of_credits_available2', 
                  'number_of_credits_required3',
                  'number_of_credits_available3', 
                  'number_of_credits_required4',
                  'number_of_credits_available4', 
                  'number_of_credits_required5',
                  'number_of_credits_available5', 
                  'number_of_credits_required6',
                  'number_of_credits_available6', 
                  'type_Scholarship_or_Student_loan_fund']
        labels = {'title' : 'คำนำหน้า', 
                  'faculty' : 'คณะ', 
                  'number_of_credits_required1' : 'หน่วยกิตที่ต้องการ 1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์', 
                  'number_of_credits_available1' : 'หน่วยกิตที่มี',
                  'number_of_credits_required2' : 'หน่วยกิตที่ต้องการ 2 ด้านกีฬาหรือการส่งเสริมสุขภาพ', 
                  'number_of_credits_available2' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required3' : 'หน่วยกิตที่ต้องการ 3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม', 
                  'number_of_credits_available3' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required4' : 'หน่วยกิตที่ต้องการ 4 ด้านเสริมสร้างคุณธรรมและจริยธรรม', 
                  'number_of_credits_available4' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required5' : 'หน่วยกิตที่ต้องการ 5 ด้านส่งเสริมศิลปะและวัฒนธรรม', 
                  'number_of_credits_available5' : 'หน่วยกิตที่มี', 
                  'number_of_credits_required6' : 'หน่วยกิตที่ต้องการ 6 ด้านกิจกรรมอื่นๆ', 
                  'number_of_credits_available6' : 'หน่วยกิตที่มี', 
                  'type_Scholarship_or_Student_loan_fund' : 'ประเภท(ทุน-กยศ)'}
        
#ที่ปรึกษาโครงการ
class UserRegisterPerson_responsible_for_the_projectRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserPerson_responsible_for_the_project
        fields = ['title', 'faculty']
        labels = {'title' : 'คำนำหน้า', 'faculty' : 'คณะ'}
    
class UserPerson_responsible_for_the_projectUpdateForm(forms.ModelForm):
    class Meta:
        model = UserPerson_responsible_for_the_project
        fields = ['title', 'faculty']
        labels = {'title': 'คำนำหน้า', 'faculty': 'คณะ'}
        
#เจ้าหน้าที่คณะ
class UserFacultyStaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserFacultyStaff
        fields = ['title', 'faculty']
        labels = {'title' : 'คำนำหน้า', 'faculty' : 'คณะ'}

class UserFacultyStaffUpdateForm(forms.ModelForm):
    class Meta:
        model = UserFacultyStaff
        fields = ['title', 'faculty']
        labels = {'title' : 'คำนำหน้า', 'faculty' : 'คณะ'}