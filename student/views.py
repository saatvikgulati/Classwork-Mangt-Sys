from django.shortcuts import render
from .models import Student
from teacher.models import Teacher
from course.models import Course
from subject.models import Subject
from answer.models import Reason
from lms1.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.
'''Saatvik
Roll No: 18030121073
BCA Sem 6
'''

def students_table(request):
    teacher=Teacher.objects.filter(teacher=request.user.id).first()
    context={
        'title':'Saatvik',
        'students':Student.objects.all(),
        'teacher_is_staff':teacher.is_staff,
    }
    return render(request,'student/students_table.html',context)

def students_in_course(request,id):
    cid=id
    current_course=Course.objects.filter(id=cid).first()
    students_list=Student.objects.filter(assigned_course=current_course)
    
    teacher=Teacher.objects.filter(teacher=request.user.id).first()
    context={
        'students':students_list,
        'teacher_is_staff':teacher.is_staff,
        
    }
    return render(request,'student/students_table.html',context)

def students_in_subject(request,id):
    sid=id
    current_subject=Subject.objects.filter(id=sid).first()
    teacher=Teacher.objects.filter(teacher=request.user.id).first()
    students_list=Student.objects.filter(assigned_subject=current_subject)
    context={
        'students':students_list,
        'teacher_is_staff':teacher.is_staff
    }
    return render(request,'student/students_table.html',context)

def student_dashboard(request):
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    if current_student is None:
        return render(request,'student/dashboard_error.html')
    context={
        'student':current_student,
        'is_student':current_student.is_student,
    }
    return render(request,'student/student_dashboard.html',context)

def sendemail_rejected(current_answer):
    current_student=current_answer.author
    recepient=current_student.student.email
    reason=Reason.objects.filter(answer=current_answer).first()
    subject="Rejected Answer "+current_answer.title
    message="Your answer "+current_answer.title+" has been rejected!!!!\nReason: \'"+reason.reason+"\'"
    send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)

def sendemail_accepted(current_answer):
    current_student=current_answer.author
    recepient=current_student.student.email
    reason=Reason.objects.filter(answer=current_answer).first()
    subject="Accepted Answer "+current_answer.title
    message="Your answer "+current_answer.title+" has been accepted!!!\nReason: \'"+reason.reason+"\'"
    send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)


def student_profiles(request):
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_student is not None:
        students_list=Student.objects.filter(assigned_course=current_student.assigned_course)
        context={
            'title':'Student Profiles',
            'is_student':current_student.is_student,
            'students_lists':students_list,
            'students':current_student,
        }
        return render(request,'student/student_profiles.html',context)
    elif current_teacher is not None:
        students_list=Student.objects.filter(assigned_course=current_teacher.assigned_course)
        context={
            'title':'Student Profiles',
            'teacher_is_staff':current_teacher.is_staff,
            'students_lists':students_list,
            'teachers':current_teacher,
        }
        return render(request,'student/student_profiles.html',context)
    else:
        context={
            'title':'Student Profiles',
        }
        return render(request,'student/student_profiles.html',context)


def my_profile(request):
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_student is not None:
        context={
            'student':current_student,
            'is_student':current_student.is_student,
        }
        return render(request,'student/my_profile.html',context)
    elif current_teacher is not None:
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'teachers':current_teacher,
        }
        return render(request,'student/my_profile.html',context)

