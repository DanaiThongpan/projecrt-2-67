# from pyexpat.errors import messages
import base64
from datetime import datetime
import os
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ActivityParticipationManagementSystem.forms import forms_activity_adduser, forms_create_activity
from ActivityParticipationManagementSystem.models import db_create_activity, db_activity_adduser
from Accounts.models import UserPerson_responsible_for_the_project, UserStudent, User
from django.contrib import messages

from Website_recruiting_students_to_participate_in_activities import settings

# Create your views here.

# Student
def is_student(user):
    return user.is_authenticated and hasattr(user, 'is_student') and user.is_student

@login_required
@user_passes_test(is_student, login_url='login')
def homeStudent(request):
    db = db_activity_adduser.objects.all()
    user_student = UserStudent.objects.get(user=request.user)
    activity_all = db_create_activity.objects.all()

    if 'show_popup' not in request.session:
        credits_needed = user_student.number_of_credits_required - user_student.number_of_credits_available

        if user_student.number_of_credits_required - user_student.number_of_credits_available <= 0:
            messages.info(
                request,
                f"ตอนนี้คุณมีหน่วยกิตครบแล้ว")
        else:
            messages.info(
                request,
                f"ตอนนี้คุณมีหน่วยกิต {user_student.number_of_credits_available} หน่วย ต้องการอีก {credits_needed} หน่วย")

        request.session['show_popup'] = True
    
    return render(request, 'Student/home.html', {
        'db': activity_all,
        'std': db,
    })

# @login_required
# @user_passes_test(is_student, login_url='login')
# def activity(request, id):
#     activity_get_id = get_object_or_404(db_create_activity, pk=id)
#     user_student = get_object_or_404(UserStudent, user=request.user)
#     existing_registration = db_activity_adduser.objects.filter(activity=activity_get_id, student=user_student).first()
#     registered_students = db_activity_adduser.objects.filter(activity=activity_get_id).select_related('student')

#     if request.method == 'POST':
#         if existing_registration:
#             # ถ้ามีการลงทะเบียนอยู่แล้ว ให้ยกเลิกการลงทะเบียน
#             existing_registration.cancel_registration()
#         else:
#             # ถ้ายังไม่ได้ลงทะเบียนและยังมีที่ว่าง ให้ลงทะเบียน
#             db_activity_adduser.objects.create(student=user_student, activity=activity_get_id)

#         return redirect('activity', id=id)

#     return render(request, 'Student/activity.html', {
#         'i': activity_get_id,
#         'existing_registration': existing_registration,
#         'registered_students': registered_students,
#         'd': user_student,
#     })

from django.db import models, transaction
from django.core.exceptions import ValidationError

@login_required
@user_passes_test(is_student, login_url='login')
def activity(request, id):
    activity_get_id = get_object_or_404(db_create_activity, pk=id)
    user_student = get_object_or_404(UserStudent, user=request.user)
    existing_registration = db_activity_adduser.objects.filter(activity=activity_get_id, student=user_student).first()
    registered_students = db_activity_adduser.objects.filter(activity=activity_get_id).select_related('student')

    def save_registration():
        """ฟังก์ชันบันทึกการลงทะเบียน"""
         # ถ้าไม่ใช่ผู้รับผิดชอบโครงการ ให้ตรวจสอบสถานะการลงทะเบียน
        if not activity_get_id.is_registration_open:
            raise ValidationError('Registration is closed for this activity.')  
        
        with transaction.atomic():
            # เพิ่มผู้ลงทะเบียนถ้ายังมีที่ว่าง
            if activity_get_id.registered_count < activity_get_id.max_participants:
                activity_get_id.registered_count += 1
                activity_get_id.save()
                db_activity_adduser.objects.create(student=user_student, activity=activity_get_id)
            else:
                raise ValidationError('No more slots available for this activity.')

    def cancel_registration():
        """ฟังก์ชันยกเลิกการลงทะเบียนและลด registered_count"""
        with transaction.atomic():
            if activity_get_id.registered_count > 0:
                activity_get_id.registered_count -= 1
                activity_get_id.is_registration_open = True  # เปิดรับสมัครอีกครั้งถ้ามีที่ว่าง
                activity_get_id.save()
            # ลบการลงทะเบียนนี้ออกจากฐานข้อมูล
            existing_registration.delete()

    if request.method == 'POST':
        if existing_registration:
            # ถ้ามีการลงทะเบียนอยู่แล้ว ให้ยกเลิกการลงทะเบียน
            cancel_registration()
        else:
            # ถ้ายังไม่ได้ลงทะเบียนและยังมีที่ว่าง ให้ลงทะเบียน
            save_registration()

        return redirect('activity', id=id)

    return render(request, 'Student/activity.html', {
        'i': activity_get_id,
        'existing_registration': existing_registration,
        'registered_students': registered_students,
        'd': user_student,
    })

def activity_history(request):
    # ดึงประวัติการเข้าร่วมกิจกรรมของผู้ใช้ที่ล็อกอินอยู่
    user = request.user
    activity_history = db_activity_adduser.objects.filter(student__user=user).select_related('activity')
    
    return render(request, 'Student/activity_history.html', {
        'activity_history': activity_history,
    })


#Person_responsible_for_the_project
def is_person_responsible_for_the_project(user):
    return user.is_authenticated and hasattr(user, 'is_person_responsible_for_the_project') and user.is_person_responsible_for_the_project

@login_required
@user_passes_test(is_person_responsible_for_the_project, login_url='login')
def homePerson_responsible_for_the_project(request):
    person_responsible = get_object_or_404(UserPerson_responsible_for_the_project, user=request.user)

    # รับค่าประเภทกิจกรรมจาก URL parameter
    activity_type = request.GET.get('activity_type', 'all')

    # ตรวจสอบว่าผู้ใช้เลือกประเภทกิจกรรมอะไร และกรองข้อมูล
    if activity_type == 'all':
        activities = db_create_activity.objects.filter(user=person_responsible)
    elif activity_type == 'academic':
        activities = db_create_activity.objects.filter(user=person_responsible, activity_type="1 ด้านวิชาการที่ส่งเสริมคุณลักษณะบัณฑิตที่พึงประสงค์")
    elif activity_type == 'sport':
        activities = db_create_activity.objects.filter(user=person_responsible, activity_type="2 ด้านกีฬาหรือการส่งเสริมสุขภาพ")
    elif activity_type == 'environment':
        activities = db_create_activity.objects.filter(user=person_responsible, activity_type="3 ด้านบำเพ็ญประโยชน์หรือรักษาสิ่งแวดล้อม")
    elif activity_type == 'moral':
        activities = db_create_activity.objects.filter(user=person_responsible, activity_type="4 ด้านเสริมสร้างคุณธรรมและจริยธรรม")
    elif activity_type == 'art_culture':
        activities = db_create_activity.objects.filter(user=person_responsible, activity_type="5 ด้านส่งเสริมศิลปะและวัฒนธรรม")
    elif activity_type == 'other':
        activities = db_create_activity.objects.filter(user=person_responsible, activity_type="6 ด้านกิจกรรมอื่นๆ")

    return render(request, 'Person_responsible_for_the_project/home.html', {
        'i': person_responsible, 
        'db': activities,
    })

@login_required
@user_passes_test(is_person_responsible_for_the_project, login_url='login')
def create_activity(request):
    user_obj = UserPerson_responsible_for_the_project.objects.get(user=request.user)
    form = forms_create_activity()
    if request.method == 'POST':
        form = forms_create_activity(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = user_obj
            activity.save()
            return redirect('homePerson_responsible_for_the_project')

    return render(request, 'Person_responsible_for_the_project/create_activity.html', {
        'form' : form
    })

from django.utils import timezone

@login_required
@user_passes_test(is_person_responsible_for_the_project, login_url='login')
def update_activity2(request, id):
    activity_get_id = db_create_activity.objects.get(pk=id)
    form = forms_create_activity(instance=activity_get_id)
    
    if request.method == 'POST':
        form = forms_create_activity(request.POST, request.FILES, instance=activity_get_id)
        
        if form.is_valid():
            activity = form.save(commit=False)

            # ตรวจสอบวันปิดรับสมัครกับวันปัจจุบัน
            if activity.due_date_registration >= timezone.now():
                activity.is_registration_open = True
            else:
                activity.is_registration_open = False

            activity.save()  # บันทึกข้อมูลกิจกรรมหลังจากตรวจสอบ
            
            return redirect('homePerson_responsible_for_the_project')
    
    # ถ้าไม่ใช่ POST method ให้แสดงฟอร์มแก้ไขกิจกรรม
    return render(request, 'Person_responsible_for_the_project/update_activity.html', {
        'form': form,
        'i': activity_get_id,
    })
# @login_required
# @user_passes_test(is_person_responsible_for_the_project, login_url='login')
# def activity_crateby_user2(request):
#     s = db_create_activity.objects.all()  
#     return render(request, 'Person_responsible_for_the_project/activitys_crateby_user.html', {
#         'db':s
#         })

def delete_activity(request, id):
    activity = get_object_or_404(db_create_activity, pk=id)
    user_obj = UserPerson_responsible_for_the_project.objects.get(user=request.user)
    if activity.user != user_obj:
        return redirect('homePerson_responsible_for_the_project')
    else:
        activity.delete()

    return redirect('homePerson_responsible_for_the_project')

def activity2(request, id):
    activity_get_id = get_object_or_404(db_create_activity, pk=id)
    registered_students = db_activity_adduser.objects.filter(activity=activity_get_id).select_related('student')

    return render(request, 'Person_responsible_for_the_project/activity.html', {
        'i': activity_get_id,
        'registered_students': registered_students,
    })

def check_student_list(request, activity_id):
    activity = get_object_or_404(db_create_activity, id=activity_id)
    
    # ดึงรายชื่อนักศึกษาที่ลงทะเบียนเข้าร่วมกิจกรรมนี้
    students_in_activity = db_activity_adduser.objects.filter(activity=activity).select_related('student')

    if request.method == 'POST':
        # ดึงรายชื่อนักศึกษาที่ถูกเลือกจาก checkbox
        selected_students = request.POST.getlist('student')
        
        # อัปเดต is_approved สำหรับนักศึกษาที่ถูกเลือก
        for student_in_activity in students_in_activity:
            if str(student_in_activity.student.id) in selected_students:
                student_in_activity.is_approved = True
            else:
                student_in_activity.is_approved = False
            
            # อัปเดตสถานะ is_approved โดยไม่ตรวจสอบสถานะการรับสมัคร
            student_in_activity.save(update_fields=['is_approved'])
        
        # ส่งข้อความแจ้งเตือนว่าอนุมัติหน่วยกิตสำเร็จ
        messages.success(request, "การอนุมัติหน่วยกิตเสร็จสมบูรณ์")
        
        # เปลี่ยนเส้นทางกลับไปที่หน้าแรก
        return redirect('homePerson_responsible_for_the_project')
    
    return render(request, 'Person_responsible_for_the_project/check_student_list.html', {
        'activity': activity,
        'students_in_activity': students_in_activity,
    })

from .models import ActivityPDF, db_activity_adduser  # นำเข้าโมเดลที่คุณต้องการใช้
from django.contrib import messages

def upload_pdf(request, activity_id):
    activity = get_object_or_404(db_create_activity, id=activity_id)

    # ตรวจสอบว่ากิจกรรมนี้มีไฟล์ PDF อัปโหลดแล้วหรือไม่
    if ActivityPDF.objects.filter(activity=activity).exists():
        messages.error(request, "PDF has already been uploaded for this activity.")
        return redirect('homePerson_responsible_for_the_project')

    if request.method == 'POST':
        # ตรวจสอบว่ามีไฟล์ที่ผู้ใช้อัปโหลดหรือไม่
        if 'pdf_file' in request.FILES:
            # สร้าง ActivityPDF object
            pdf_file = request.FILES['pdf_file']
            ActivityPDF.objects.create(activity=activity, pdf_file=pdf_file)
            messages.success(request, "PDF uploaded successfully.")
            return redirect('homePerson_responsible_for_the_project')
        else:
            messages.error(request, "No file selected.")
            return redirect('homePerson_responsible_for_the_project')

    return render(request, 'Person_responsible_for_the_project/home.html', {'activity': activity})

def delete_pdf(request, pdf_id):
    # ดึง PDF ที่ต้องการลบ
    pdf = get_object_or_404(ActivityPDF, id=pdf_id)
    
    # ลบไฟล์ PDF
    pdf.pdf_file.delete()  # ลบไฟล์ที่เก็บใน storage
    pdf.delete()  # ลบ record ออกจาก database

    messages.success(request, "ลบไฟล์ PDF สำเร็จ")
    
    # กลับไปยังหน้าที่ต้องการหลังจากลบแล้ว (อาจเปลี่ยนเป็นหน้าที่เหมาะสมตามโครงสร้างระบบของคุณ)
    return redirect('homePerson_responsible_for_the_project')

import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import db_activity_adduser

def generate_pdf(request, id):
    # ดึงข้อมูลจากฐานข้อมูลโดยใช้ activity_id
    db_user = db_activity_adduser.objects.filter(activity_id=id)

    # สร้าง buffer เพื่อเก็บข้อมูลของไฟล์ PDF
    buffer = BytesIO()

    # สร้าง PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    
    story = []

    # ระบุพาธฟอนต์ที่ถูกต้อง
    font_path = os.path.join(settings.BASE_DIR, 'ActivityParticipationManagementSystem', 'path_to_fonts', 'THSarabunNew.ttf')

    # ตรวจสอบว่าฟอนต์มีอยู่จริงหรือไม่
    if not os.path.exists(font_path):
        return HttpResponse(f"Font file not found at {font_path}", status=404)

    # ลงทะเบียนฟอนต์ภาษาไทย
    pdfmetrics.registerFont(TTFont('THSarabunNew', font_path))

    # สร้างสไตล์ที่รองรับภาษาไทย
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ThaiStyle', fontName='THSarabunNew', fontSize=16, leading=20))
    styles.add(ParagraphStyle(name='TableHeaderStyle', fontName='THSarabunNew', fontSize=14, alignment=1))
    styles.add(ParagraphStyle(name='TableCellStyle', fontName='THSarabunNew', fontSize=14, alignment=0))
    styles.add(ParagraphStyle(name='CenteredStyle', fontName='THSarabunNew', fontSize=16, alignment=1))

    # หัวข้อรายงาน
    if db_user.exists():
        activity_name = db_user.first().activity.activity_name
        place = db_user.first().activity.place

        # เพิ่มหัวข้อในตาราง
        story.append(Paragraph(f"รายชื่อผู้เข้าร่วมกิจกรรม {activity_name}", styles['CenteredStyle']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("วันที่ 16 สิงหาคม 2566", styles['CenteredStyle']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("เวลา 11.00 น. - 16.00 น.", styles['CenteredStyle']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"ณ {db_user.first().activity.place}", styles['CenteredStyle']))
        story.append(Spacer(1, 24))
        story.append(Spacer(1, 24))
        
        # สร้างหัวตาราง
        data = [['ลำดับ', 'ชื่อ-สกุล', 'รหัสนักศึกษา', 'คณะ', 'ลงชื่อ']]

        # เพิ่มข้อมูลในตาราง
        for index, user in enumerate(db_user, start=1):
            full_name = f"{user.student.title} {user.student.user.first_name} {user.student.user.last_name}"
            student_id = user.student.user.username
            faculty = user.student.faculty
            data.append([str(index), full_name, student_id, faculty, ""])

        # สร้างตาราง
        table = Table(data, colWidths=[50, 150, 100, 100, 100])

        # กำหนดสไตล์ให้กับตาราง
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'THSarabunNew'),  # ใช้ฟอนต์ไทยสำหรับทั้งตาราง
            ('FONTSIZE', (0, 0), (-1, 0), 16),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))

        # เพิ่มตารางลงในเนื้อหา
        story.append(table)

    else:
        story.append(Paragraph("ไม่พบข้อมูลผู้เข้าร่วมกิจกรรม", styles['CenteredStyle']))

    # สร้าง PDF จากเนื้อหา
    pdf.build(story)

    # ดึงข้อมูล PDF จาก buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # เข้ารหัสเป็น base64 เพื่อให้สามารถฝังลงใน HTML ได้
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

    # ส่งข้อมูล PDF และ activity_id ไปยัง template HTML
    return render(request, 'Person_responsible_for_the_project/generate_pdf.html', {'pdf_base64': pdf_base64, 'activity_id': id})

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from django.http import HttpResponse
from io import BytesIO
import os
from django.conf import settings
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def generate_registration_form(request, id):

    db_user = db_activity_adduser.objects.filter(activity_id=id)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Path to Thai font
    font_path = os.path.join(settings.BASE_DIR, 'ActivityParticipationManagementSystem', 'path_to_fonts', 'THSarabunNew.ttf')
    
    # Register Thai font
    pdfmetrics.registerFont(TTFont('THSarabunNew', font_path))
    pdf.setFont("THSarabunNew", 14)

    # Set up the PDF document
    pdf.setTitle("Activity Participation Form")

    # T# Title
    pdf.drawCentredString(10.5 * cm, 28.5 * cm, "แบบบันทึกการเข้าร่วมกิจกรรมของนักศึกษามหาวิทยาลัยอุบลราชธานี")

    # ชื่อกิจกรรม (ภาษาไทย)
    pdf.drawString(2 * cm, 27.5 * cm, "ชื่อกิจกรรม (ภาษาไทย):")
    pdf.drawString(6.5 * cm, 27.5 * cm, db_user.first().activity.activity_name)
    pdf.line(6.5 * cm, 27.3 * cm, 18 * cm, 27.3 * cm)

    # ชื่อกิจกรรม (ภาษาอังกฤษ)
    pdf.drawString(2 * cm, 26.7 * cm, "ชื่อกิจกรรม (ภาษาอังกฤษ):")  # ลดช่องไฟลงเล็กน้อย
    pdf.drawString(6.5 * cm, 26.7 * cm, "")
    pdf.line(6.5 * cm, 26.5 * cm, 18 * cm, 26.5 * cm)

    # หน่วยงานที่จัดกิจกรรม
    pdf.drawString(2 * cm, 25.9 * cm, "หน่วยงานที่จัดกิจกรรม:")  # ลดช่องไฟลงเล็กน้อย

    # Draw checkboxes and text for "หน่วยงานที่จัดกิจกรรม"
    pdf.rect(7 * cm, 25.7 * cm, 0.4 * cm, 0.4 * cm)  # ลดช่องไฟลงเล็กน้อย
    pdf.drawString(7.5 * cm, 25.8 * cm, "หน่วยงานภายใน")
    pdf.line(7.1 * cm, 25.8 * cm, 7.3 * cm, 26 * cm)

    pdf.rect(12 * cm, 25.7 * cm, 0.4 * cm, 0.4 * cm)  # ลดช่องไฟลงเล็กน้อย
    pdf.drawString(12.5 * cm, 25.8 * cm, "หน่วยงานภายนอก")

    pdf.drawString(7 * cm, 25.1 * cm, "โปรดระบุชื่อหน่วยงาน:")  # ลดช่องไฟลงเล็กน้อย
    pdf.line(10 * cm, 25.1 * cm, 18 * cm, 25.1 * cm)
    pdf.drawString(11 * cm, 25.3 * cm, "")

    # ด้านกิจกรรม
    pdf.drawString(2 * cm, 24.3 * cm, "ด้านกิจกรรม:")  # ลดช่องไฟลงเล็กน้อย

    # วิชาการที่ส่งเสริมคุณลักษณะบัณฑิต
    pdf.rect(4 * cm, 24.1 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(5 * cm, 24.3 * cm, "วิชาการที่ส่งเสริมคุณลักษณะบัณฑิต")
    pdf.drawString(5 * cm, 23.8 * cm, "ที่พึงประสงค์")

    # กีฬา หรือการส่งเสริมสุขภาพ
    pdf.rect(4 * cm, 23.3 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(5 * cm, 23.3 * cm, "กีฬา หรือการส่งเสริมสุขภาพ")

    # บำเพ็ญประโยชน์ หรือรักษาสิ่งแวดล้อม
    pdf.rect(4 * cm, 22.5 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(5 * cm, 22.5 * cm, "บำเพ็ญประโยชน์ หรือรักษาสิ่งแวดล้อม")

    # เสริมสร้างคุณธรรม และจริยธรรม
    pdf.rect(4 * cm, 21.7 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(5 * cm, 21.7 * cm, "เสริมสร้างคุณธรรม และจริยธรรม")

    # ส่งเสริมศิลปะ และวัฒนธรรม
    pdf.rect(4 * cm, 20.9* cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(5 * cm, 20.9 * cm, "ส่งเสริมศิลปะ และวัฒนธรรม")

    # ด้านกิจกรรมตาม TQF
    pdf.rect(14 * cm, 24.1 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(10.5 * cm, 24.3 * cm, "ด้านกิจกรรมตาม TQF:")
    pdf.drawString(15 * cm, 24.3 * cm, "ด้านคุณธรรมจริยธรรม")

    # ด้านความรู้
    pdf.rect(14 * cm, 23.3 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(15 * cm, 23.5 * cm, "ด้านความรู้")

    # ด้านทักษะทางปัญญา
    pdf.rect(14 * cm, 22.5 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(15 * cm, 22.7 * cm, "ด้านทักษะทางปัญญา")

    # ด้านความสัมพันธ์ระหว่างบุคคล และความรับผิดชอบ
    pdf.rect(14 * cm, 21.7 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(15 * cm, 21.9 * cm, "ด้านความสัมพันธ์ระหว่างบุคคล")
    pdf.drawString(15 * cm, 21.4 * cm, "ความรับผิดชอบ")

    # ด้านการวิเคราะห์เชิงตัวเลข การสื่อสาร และการใช้เทคโนโลยี สารสนเทศ
    pdf.rect(14 * cm, 20.5 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(15 * cm, 20.9 * cm, "ด้านการวิเคราะห์เชิงตัวเลข การสื่อสาร")
    pdf.drawString(15 * cm, 20.4 * cm, "และการใช้เทคโนโลยี สารสนเทศ")

    # จำนวนชั่วโมงที่เข้าร่วมกิจกรรม
    pdf.drawString(2 * cm, 19.5 * cm, "จำนวนชั่วโมงที่เข้าร่วมกิจกรรม:")  # ปรับตำแหน่งขึ้นเล็กน้อย
    pdf.drawString(6.7 * cm, 19.5 * cm, "")
    pdf.line(6.5 * cm, 19.4 * cm, 7.5 * cm, 19.4 * cm)
    pdf.drawString(8 * cm, 19.5 * cm, "ชั่วโมง")

    # จำนวนผู้เข้าร่วม (เป้าหมาย)
    pdf.drawString(10.5 * cm, 19.5 * cm, "จำนวนผู้เข้าร่วม (เป้าหมาย):")
    pdf.drawString(15.5 * cm, 19.5 * cm, "")
    pdf.line(15 * cm, 19.4 * cm, 16 * cm, 19.4 * cm)
    pdf.drawString(16.5 * cm, 19.5 * cm, "คน")

    # วันที่เริ่มและสิ้นสุดกิจกรรม
    pdf.drawString(2 * cm, 18.5 * cm, "วันที่เริ่ม:")  # ปรับตำแหน่งขึ้นเล็กน้อย
    pdf.drawString(4 * cm, 18.5 * cm, "")
    pdf.line(3.8 * cm, 18.4 * cm, 6.5 * cm, 18.4 * cm)
    pdf.drawString(7.5 * cm, 18.5 * cm, "เวลา")
    pdf.drawString(8.5 * cm, 18.5 * cm, "")
    pdf.line(8.4 * cm, 18.4 * cm, 10 * cm, 18.4 * cm)

    pdf.drawString(11 * cm, 18.5 * cm, "วันที่สิ้นสุด:")
    pdf.drawString(13 * cm, 18.5 * cm, "")
    pdf.line(12.8 * cm, 18.4 * cm, 15.5 * cm, 18.4 * cm)
    pdf.drawString(15.7 * cm, 18.5 * cm, "เวลา")
    pdf.drawString(17.5 * cm, 18.5 * cm, "")
    pdf.line(17.4 * cm, 18.4 * cm, 19 * cm, 18.4 * cm)

    # ผู้รับผิดชอบโครงการ และที่ปรึกษาโครงการ
    pdf.drawString(2 * cm, 17.5 * cm, "ผู้รับผิดชอบโครงการ:")
    pdf.drawString(6 * cm, 17.5 * cm, "")
    pdf.line(5.8 * cm, 17.4 * cm, 10.5 * cm, 17.4 * cm)

    pdf.drawString(11 * cm, 17.5 * cm, "ที่ปรึกษาโครงการ:")
    pdf.line(14.5 * cm, 17.4 * cm, 19 * cm, 17.4 * cm)

    # สถานที่จัดกิจกรรม
    pdf.drawString(2 * cm, 16.5 * cm, "สถานที่จัดกิจกรรม:")
    pdf.drawString(5.5 * cm, 16.5 * cm, "")
    pdf.line(5.3 * cm, 16.4 * cm, 20.5 * cm, 16.4 * cm)

    # งบประมาณ
    pdf.drawString(2 * cm, 16 * cm, "งบประมาณ")

    # เงินงบประมาณแผ่นดิน
    pdf.rect(4 * cm, 15.8 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(4.7 * cm, 15.8 * cm, "เงินงบประมาณแผ่นดิน")
    pdf.line(9.5 * cm, 15.8 * cm, 11.5 * cm, 15.8 * cm)

    # เงินรายได้มหาวิทยาลัย
    pdf.rect(4 * cm, 15 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(4.7 * cm, 15 * cm, "เงินรายได้มหาวิทยาลัย")
    pdf.line(9.5 * cm, 15 * cm, 11.5 * cm, 15 * cm)

    # เงินรายได้อื่นๆ (โปรดระบุ)
    pdf.rect(4 * cm, 14.2 * cm, 0.4 * cm, 0.4 * cm)
    pdf.drawString(4.7 * cm, 14.2 * cm, "เงินรายได้อื่นๆ (โปรดระบุ)")
    pdf.line(9.5 * cm, 14.2 * cm, 18.5 * cm, 14.2 * cm)

    # คำอธิบายเกี่ยวกับกิจกรรม
    pdf.drawString(2 * cm, 13.7 * cm, "คำอธิบายเกี่ยวกับกิจกรรม")
    pdf.line(2 * cm, 13.2 * cm, 18 * cm, 13.2 * cm)
    pdf.line(2 * cm, 12.7 * cm, 18 * cm, 12.7 * cm)
    pdf.line(2 * cm, 12.2 * cm, 18 * cm, 12.2 * cm)

    # รายชื่อนักศึกษาที่เข้าร่วม (ต่อท้ายคำอธิบาย)
    pdf.drawString(2 * cm, 11.5 * cm, "รายชื่อนักศึกษาที่เข้าร่วม")
    pdf.drawString(2 * cm, 11 * cm, "(กรุณาระบุ ชื่อ-สกุล คณะ รหัสนักศึกษา หมายเลขติดต่อให้ครบถ้วน)")
    pdf.line(2 * cm, 10.5 * cm, 18 * cm, 10.5 * cm)
    pdf.line(2 * cm, 10 * cm, 18 * cm, 10 * cm)
    pdf.line(2 * cm, 9.5 * cm, 18 * cm, 9.5 * cm)

    # หมายเหตุ
    pdf.drawString(2 * cm, 8.5 * cm, "หมายเหตุ: โปรดแนบหลักฐานการเข้าร่วมกิจกรรม เช่น สําเนาโครงการ หนังสือเชิญ กําหนดการ รูปถ่าย เป็นต้น")
    pdf.drawString(2 * cm, 8 * cm, "กรณีมีจํานวนนักศึกษาที่เข้าร่วมจํานวนมาก ให้แนบรายชื่อนักศึกษาพร้อมแบบบันทึกและชื่อรับรองทุกแผ่น")
    (2 * cm, 4.5 * cm, "กรณีมีจํานวนนักศึกษาที่เข้าร่วมจํานวนมาก ให้แนบรายชื่อนักศึกษาพร้อมแบบบันทึกและชื่อรับรองทุกแผ่น")

    # Save the PDF
    pdf.showPage()
    pdf.save()

    # Get the value of the BytesIO buffer and return it as a response
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # เข้ารหัสเป็น base64 เพื่อให้สามารถฝังลงใน HTML ได้
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

    # ส่งข้อมูล PDF และ activity_id ไปยัง template HTML
    return render(request, 'Person_responsible_for_the_project/generate_registration_form.html', {'pdf_base64': pdf_base64, 'activity_id': id})


def homeFacultyStaff(request):
    activity = db_create_activity.objects.all()
    
    # ตรวจสอบว่ามีการกดปุ่มอนุมัติหรือไม่
    if request.method == 'POST':
        if 'approve_activity' in request.POST:
            activity_id = request.POST.get('approve_activity')
            selected_activity = get_object_or_404(db_create_activity, id=activity_id)
            
            # ตรวจสอบว่ายังไม่ได้รับการอนุมัติ
            if not selected_activity.is_approved:
                # เลือกเฉพาะนักศึกษาที่มี is_approved = True
                students_in_activity = db_activity_adduser.objects.filter(activity=selected_activity, is_approved=True).select_related('student')
                
                for student_in_activity in students_in_activity:
                    student = student_in_activity.student
                    student.number_of_credits_available += selected_activity.credit
                    student.save()

                selected_activity.is_approved = True  # อัปเดตสถานะการอนุมัติ
                selected_activity.save()
                messages.success(request, "นักศึกษาที่ได้รับการอนุมัติในกิจกรรมนี้ได้รับเครดิตแล้ว")
            else:
                messages.warning(request, "กิจกรรมนี้ได้รับการอนุมัติแล้ว")

        elif 'cancel_approval' in request.POST:
            activity_id = request.POST.get('cancel_approval')
            selected_activity = get_object_or_404(db_create_activity, id=activity_id)
            
            # ตรวจสอบว่ากิจกรรมได้รับการอนุมัติแล้ว และทำการยกเลิกอนุมัติ
            if selected_activity.is_approved:
                # เลือกเฉพาะนักศึกษาที่มี is_approved = True
                students_in_activity = db_activity_adduser.objects.filter(activity=selected_activity, is_approved=True).select_related('student')
                
                for student_in_activity in students_in_activity:
                    student = student_in_activity.student
                    student.number_of_credits_available -= selected_activity.credit  # ลบเครดิต
                    student.save()

                selected_activity.is_approved = False  # ยกเลิกสถานะการอนุมัติ
                selected_activity.save()
                messages.success(request, "ยกเลิกการอนุมัติเรียบร้อยแล้ว")
            else:
                messages.warning(request, "กิจกรรมนี้ยังไม่ได้รับการอนุมัติ")

    return render(request, 'FacultyStaff/home.html', {
        'db': activity,
    })

from django.http import JsonResponse
from django.db.models import Count

def dashboard(request):
    selected_type = request.GET.get('activity_type', '')  # รับค่าที่ผู้ใช้เลือกจาก Dropdown
    # นับจำนวนการเข้าร่วมกิจกรรมแบ่งตามประเภทกิจกรรม
    activity_stats = db_create_activity.objects.values('activity_type').annotate(count=Count('id'))
    activities = db_create_activity.objects.all()

    if selected_type:
        activities = activities.filter(activity_type=selected_type)

    activity_types = db_create_activity.objects.values_list('activity_type', flat=True).distinct()

    for activity in activities:
        if activity.max_participants > 0:
            activity.participation_percentage = (activity.registered_count / activity.max_participants) * 100
        else:
            activity.participation_percentage = 0  

   
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'activityLabels': [activity.activity_name for activity in activities],
            'maxParticipantsData': [activity.max_participants for activity in activities],
            'registeredCountData': [activity.registered_count for activity in activities],
            'activities': [
                {
                    'activity_name': activity.activity_name,
                    'max_participants': activity.max_participants,
                    'registered_count': activity.registered_count,
                    'participation_percentage': activity.participation_percentage,
                }
                for activity in activities
            ]
        }
        return JsonResponse(data)

    return render(request, 'FacultyStaff/dashboard.html', {
        'activity_stats': activity_stats,
        'activities': activities,
        'activity_types': activity_types,  
        'selected_type': selected_type,
    })

def approve_credits(request, activity_id):
    activity = get_object_or_404(db_create_activity, id=activity_id)
    
    students_in_activity = db_activity_adduser.objects.filter(activity=activity).select_related('student')
    
    for student_in_activity in students_in_activity:
        student = student_in_activity.student
        student.number_of_credits_available += activity.credit
        student.save()

    messages.success(request, "นักศึกษาทุกคนได้รับเครดิตเรียบร้อยแล้ว")
    return redirect('homeFacultyStaff')
