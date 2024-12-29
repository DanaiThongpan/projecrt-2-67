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
        fields = ['title', 'faculty', 'number_of_credits_required','number_of_credits_available', 'type_Scholarship_or_Student_loan_fund']
        labels = {'title' : 'คำนำหน้า', 'faculty' : 'คณะ', 'number_of_credits_required' : 'หน่วยกิตที่ต้องการ', 'number_of_credits_available' : 'หน่วยกิตที่มี', 'type_Scholarship_or_Student_loan_fund' : 'ประเภท(ทุน-กยศ)'}
        
class UserStudentUpdateForm(forms.ModelForm):
    class Meta:
        model = UserStudent
        fields = ['title', 'faculty', 'number_of_credits_required', 'number_of_credits_available', 'type_Scholarship_or_Student_loan_fund']
        labels = {'title': 'คำนำหน้า', 'faculty': 'คณะ', 'number_of_credits_required': 'หน่วยกิตที่ต้องการ', 'number_of_credits_available': 'หน่วยกิตที่มี', 'type_Scholarship_or_Student_loan_fund': 'ประเภท (ทุน-กยศ)'}
        
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