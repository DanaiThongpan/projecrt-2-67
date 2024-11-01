from django.contrib import admin
from ActivityParticipationManagementSystem.models import ActivityPDF, db_create_activity, db_activity_adduser

# Register your models here.
class DbCreateActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 
                    'img_activity', 
                    'activity_name', 
                    'activity_type', 
                    # 'start_date_create_activity', 
                    # 'due_date_create_activity', 
                    'due_date_registration',
                    'place', 
                    'start_date_activity', 
                    'due_date_activity', 
                    'description', 
                    'credit'
                    )

admin.site.register(db_create_activity, DbCreateActivityAdmin)

class db_activity_adduserAdmin(admin.ModelAdmin):
    list_display = ('student', 
                    'activity_id',
                    'is_approved',
                    )

admin.site.register(db_activity_adduser, db_activity_adduserAdmin)

class ActivityPDFAdmin(admin.ModelAdmin):
    list_display = ('activity', 
                    'pdf_file'
                    )

admin.site.register(ActivityPDF, ActivityPDFAdmin)