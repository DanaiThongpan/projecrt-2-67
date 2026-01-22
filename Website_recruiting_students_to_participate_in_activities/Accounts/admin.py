from django.contrib import admin
from Accounts.models import UserStudent, UserPerson_responsible_for_the_project, User, UserFacultyStaff

# Register your models here.
class UserDisplay(admin.ModelAdmin):
    list_display = ['username', 
                    'email', 
                    'first_name', 
                    'last_name', 
                    'is_staff', 
                    'is_student', 
                    'is_person_responsible_for_the_project',
                    'is_faculty_staff']

admin.site.register(User, 
                    UserDisplay)

class UserStudentAdminDisplay(admin.ModelAdmin):
    list_display = ['title', 
                    'faculty', 
                    'type_Scholarship_or_Student_loan_fund', 
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
                    'number_of_credits_available6']

admin.site.register(UserStudent, 
                    UserStudentAdminDisplay,
                    )

class UserPerson_responsible_for_the_projectAdminDisplay(admin.ModelAdmin):
    list_display = ['user',
                    'title', 
                    'faculty']

admin.site.register(UserPerson_responsible_for_the_project, UserPerson_responsible_for_the_projectAdminDisplay)

class UserUserFacultyStaffAdminDisplay(admin.ModelAdmin):
    list_display = ['user',
                    'title', 
                    'faculty',
                    'is_approved']

admin.site.register(UserFacultyStaff, UserUserFacultyStaffAdminDisplay)