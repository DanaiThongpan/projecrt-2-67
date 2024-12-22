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
    path('homePerson_responsible_for_the_project/delete_pdf/<int:pdf_id>/', delete_pdf, name='delete_pdf'),

    path('homePerson_responsible_for_the_project/generate_pdf/<int:id>/', generate_pdf, name='generate_pdf'),
    path('homePerson_responsible_for_the_project/generate_registration_form/<int:id>/', generate_registration_form, name='generate_registration_form'),
    path('homePerson_responsible_for_the_project/<int:activity_id>/check_student_list/', check_student_list, name='check_student_list'),

    path('homeFacultyStaff/', homeFacultyStaff, name='homeFacultyStaff'),
    path('dashboard/', dashboard, name='dashboard'),
    path('activity/<int:activity_id>/upload_pdf/', upload_pdf, name='upload_pdf'),
    
    path('approve_credits/<int:activity_id>/', approve_credits, name='approve_credits'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)