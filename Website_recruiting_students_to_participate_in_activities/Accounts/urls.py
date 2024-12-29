from django.urls import path
from Accounts.views import *

urlpatterns = [
    path('', home, name='home'),
    
    path('login/', login, name='login'),
    path('Register/', Register, name='Register'),
    path('RegisterFacultyStaff/', RegisterFacultyStaff, name='RegisterFacultyStaff'),
    path('logout/', logout, name='logout'),

    path('Accounts/profileStudent', profileStudent, name='profileStudent'),
    path('Accounts/updateprofileStudent/<int:id>/', updateprofileStudent, name='updateprofileStudent'),

    path('Accounts/profilePerson_responsible_for_the_project', profilePerson_responsible_for_the_project, name='profilePerson_responsible_for_the_project'),
    path('Accounts/updateprofilePerson_responsible_for_the_project/<int:id>/', updateprofilePerson_responsible_for_the_project, name='updateprofilePerson_responsible_for_the_project'),

    path('Accounts/profileFacultyStaff', profileFacultyStaff, name='profileFacultyStaff'),
    path('Accounts/updateprofileFacultyStaff/<int:id>/', updateprofileFacultyStaff, name='updateprofileFacultyStaff'),
]