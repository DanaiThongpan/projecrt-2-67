from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login as auth_login, logout as auth_logout)
from Accounts.models import *
from ActivityParticipationManagementSystem.models import db_create_activity
from .forms import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def home(request):
    activity_all = db_create_activity.objects.all()
    
    return render(request, 'Accounts/home.html', {
        'activity_all' : activity_all
    })

def Register(request):
    role = request.GET.get('role')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if role == 'student':
            form2 = UserStudentrRegistrationForm(request.POST)
        else:
            form2 = UserRegisterPerson_responsible_for_the_projectRegistrationForm(request.POST)

        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            if role == 'student':
                user.is_student = True
                user.save()
                student_profile = form2.save(commit=False)
                student_profile.user = user
                student_profile.save()
            elif role == 'person_responsible_for_the_project':
                user.is_person_responsible_for_the_project = True
                user.save()
                person_responsible_profile = form2.save(commit=False)
                person_responsible_profile.user = user
                person_responsible_profile.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
        if role == 'student':
            form2 = UserStudentrRegistrationForm()
        else:
            form2 = UserRegisterPerson_responsible_for_the_projectRegistrationForm()

    return render(request, 'Accounts/register.html', {
        'form1': form,
        'form2': form2,
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if request.user.is_staff:
                return redirect('homeFacultyStaff')
            elif request.user.is_person_responsible_for_the_project:
                return redirect('homePerson_responsible_for_the_project')
            elif request.user.is_student:
                return redirect('homeStudent')
            else:
                return redirect('/')
            
    return render(request, 'Accounts/login.html')

@login_required
def logout(request):
    auth_logout(request)

    return redirect('login')

def is_student(user):

    return user.is_authenticated and hasattr(user, 'is_student') and user.is_student

@login_required
@user_passes_test(is_student, login_url='login')
def updateprofileStudent(request, id):
    user_student = get_object_or_404(UserStudent, pk=id)
    user_form = UserUpdateForm(instance=user_student.user)
    student_form = UserStudentrUpdateForm(instance=user_student)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user_student.user)
        student_form = UserStudentrUpdateForm(request.POST, instance=user_student)
        
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            return redirect('profileStudent')
    
    return render(request, 'ProfileStudent/updateprofileStudent.html', {
        'form1': student_form,
        'form2': user_form,
        'id_user_student' : user_student
    })

@login_required
@user_passes_test(is_student, login_url='login')
def profileStudent(request):
    user_student = UserStudent.objects.get(user=request.user)
    student_detail = UserStudent.objects.get(pk=user_student.id)
    user_detail = request.user

    return render(request, 'ProfileStudent/profileStudent.html', {
        'student_detail' : student_detail,
        'user_detail' : user_detail,
    })

def is_person_responsible_for_the_project(user):

    return user.is_authenticated and hasattr(user, 'is_person_responsible_for_the_project') and user.is_person_responsible_for_the_project

@login_required
@user_passes_test(is_person_responsible_for_the_project, login_url='login')
def profilePerson_responsible_for_the_project(request):
    user_person_responsible_for_the_project = UserPerson_responsible_for_the_project.objects.get(user=request.user)
    person_responsible_for_the_project_detail = UserPerson_responsible_for_the_project.objects.get(pk=user_person_responsible_for_the_project.id)
    user_detail = request.user

    return render(request, 'ProfilePerson_responsible_for_the_project/profilePerson_responsible_for_the_project.html', {
        'person_responsible_for_the_project_detail' : person_responsible_for_the_project_detail,
        'user_detail' : user_detail,
    })

@login_required
@user_passes_test(is_person_responsible_for_the_project, login_url='login')
def updateprofilePerson_responsible_for_the_project(request, id):
    user_person_responsible_for_the_project = get_object_or_404(UserPerson_responsible_for_the_project, pk=id)
    user_form = UserUpdateForm(instance=user_person_responsible_for_the_project.user)
    person_responsible_for_the_project_form = UserPerson_responsible_for_the_projectUpdateForm(instance=user_person_responsible_for_the_project)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user_person_responsible_for_the_project.user)
        person_responsible_for_the_project_form = UserPerson_responsible_for_the_projectUpdateForm(request.POST, instance=user_person_responsible_for_the_project)
        
        if user_form.is_valid() and person_responsible_for_the_project_form.is_valid():
            user_form.save()
            person_responsible_for_the_project_form.save()
            return redirect('profilePerson_responsible_for_the_project')
    
    return render(request, 'ProfilePerson_responsible_for_the_project/updateprofileProfilePerson_responsible_for_the_project.html', {
        'form1': person_responsible_for_the_project_form,
        'form2': user_form,
        'id_user_person_responsible_for_the_project': user_person_responsible_for_the_project,
    })