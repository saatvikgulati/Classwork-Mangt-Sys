from django.shortcuts import render
from .models import Subject
from teacher.models import Teacher
from student.models import Student
# Create your views here.
'''Saatvik
Roll No: 18030121073
BCA Sem 6
'''

def subject_detail(request,id):
    sid=id
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_subject=Subject.objects.filter(id=sid).first()
    context={
        'current_subject':current_subject,
        'teacher_is_staff':current_teacher.is_staff,
    }
    return render(request,'subject/subject_detail.html',context)

def subjects_table_student(request):
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_subject=current_student.assigned_subject.all()
    context={
        'current_subject':current_subject,
        'is_student':current_student.is_student,
    }
    return render(request,'subject/subject_table_student.html',context)