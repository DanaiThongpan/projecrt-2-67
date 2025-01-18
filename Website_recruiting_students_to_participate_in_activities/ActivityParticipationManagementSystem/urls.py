from django.urls import path
from ActivityParticipationManagementSystem.views import *
from django.conf.urls.static import static
from Website_recruiting_students_to_participate_in_activities import settings
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path('homeStudent/', homeStudent, name='homeStudent'),
    path('homePerson_responsible_for_the_project/', homePerson_responsible_for_the_project, name='homePerson_responsible_for_the_project'),
    path('homeStudent/activity/<int:id>/', activity, name='activity'),
    path('homeStudent/activity_history/', activity_history, name='activity_history'),

    # URL สำหรับดาวน์โหลดไฟล์ CSV
    path('download_csv/<int:activity_id>/', download_activity_csv, name='download_activity_csv'),

    path('create_activity/', create_activity, name='create_activity'),
    path('homePerson_responsible_for_the_project/activity2/<int:id>/', activity2, name="activity2"),
    path('homePerson_responsible_for_the_project/update_activity/<int:id>/', update_activity2, name="update_activity2"),
    # path('activity_crateby_user2/', activity_crateby_user2, name='activity_crateby_user2'),

    path('homePerson_responsible_for_the_project/delete_activity/<int:id>/', delete_activity, name='delete_activity'),
    path('homeActivity/delete_activity2/<int:id>/', delete_activity2, name='delete_activity2'),

    path('homePerson_responsible_for_the_project/delete_pdf/<int:pdf_id>/', delete_pdf, name='delete_pdf'),

    path('homeActivity/delete_pdf2/<int:pdf_id>/', delete_pdf2, name='delete_pdf2'),

    path('homePerson_responsible_for_the_project/generate_pdf/<int:id>/', generate_pdf, name='generate_pdf'),
    path('homePerson_responsible_for_the_project/generate_registration_form/<int:id>/', generate_registration_form, name='generate_registration_form'),
    path('homePerson_responsible_for_the_project/<int:activity_id>/check_student_list/', check_student_list, name='check_student_list'),

    path('homeFacultyStaff/', homeFacultyStaff, name='homeFacultyStaff'),
    path('homeActivity/', homeActivity, name='homeActivity'),
    path('create_activity_by_faculty_staff/', create_activity_by_faculty_staff, name='create_activity_by_faculty_staff'),

    path('homeActivity/generate_pdf2/<int:id>/', generate_pdf2, name='generate_pdf2'),
    path('homeActivity/generate_registration_form2/<int:id>/', generate_registration_form2, name='generate_registration_form2'),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard2/', dashboard2, name='dashboard2'),
    path('activity/<int:activity_id>/upload_pdf/', upload_pdf, name='upload_pdf'),
    path('activity/<int:activity_id>/upload_pdf2/', upload_pdf2, name='upload_pdf2'),
    
    # path('approve_credits/<int:activity_id>/', approve_credits, name='approve_credits'),

    path('homeAdmin/', homeAdmin, name='homeAdmin'),
    path('dashboard_api/', dashboard_api, name='dashboard_api'),
    # path('approve_user/<int:user_id>/', approve_user, name='approve_user'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)