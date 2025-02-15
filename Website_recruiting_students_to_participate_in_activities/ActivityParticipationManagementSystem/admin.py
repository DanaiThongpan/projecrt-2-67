from django.contrib import admin
from ActivityParticipationManagementSystem.models import *

# Register your models here.
class DbCreateActivityAdmin(admin.ModelAdmin):
    list_display = ('announcement_date',
                    'semester',
                    'is_approved',
                    'img_activity', 
                    'activity_name', 
                    'activity_type', 
                    'due_date_registration',
                    'description', 
                    'credit',
                    )

admin.site.register(db_create_activity, DbCreateActivityAdmin)

class TimeEventAdmin(admin.ModelAdmin):
    list_display = ('activity_id', 
                    'start_date_activity',
                    'due_date_activity',
                    'place',
                    )

admin.site.register(TimeEvent, TimeEventAdmin)

class db_activity_adduserAdmin(admin.ModelAdmin):
    list_display = ('student', 
                    # 'TimeEvent',
                    'activity_id',
                    'is_approved',
                    )

admin.site.register(db_activity_adduser, db_activity_adduserAdmin)

class ActivityPDFAdmin(admin.ModelAdmin):
    list_display = ('activity', 
                    'pdf_file',
                    )

admin.site.register(ActivityPDF, ActivityPDFAdmin)