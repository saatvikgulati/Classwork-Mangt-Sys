from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Teacher
from student.models import Student
from course.models import Course
from subject.models import Subject
from django.contrib.auth.decorators import login_required
#from .forms import TeacherRegisterForm

# Create your views here.
'''Saatvik
Roll No: 18030121073
BCA Sem 6
'''


def facultydashboard(request):
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    if current_teacher is None:
        return render(request,'teacher/dashboard_error.html')
    context={
        'posts':Student.objects.all(),
        'teacher_is_staff':current_teacher.is_staff,
        'current_teacher':current_teacher
        # 'teacher_faculty_list':Teacher.objects.all()
    }
    return render(request,'teacher/faculty_dashboard.html',context)


def faculty_table(request):
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    if current_teacher is not None:
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'teachers':Teacher.objects.all(),
        }
        return render(request,'teacher/faculty_table.html',context)
    else:
        context={
            'is_student':current_student.is_student,
            'teachers':Teacher.objects.all(),
        }
        return render(request,'teacher/faculty_table.html',context)

def faculty_by_course(request,id):
    object=Teacher.objects.filter(teacher=request.user.id).first()
    cid=id
    current_course=Course.objects.filter(id=cid).first()
    teachers=Teacher.objects.filter(assigned_course=current_course)
    context={
        'teacher_is_staff':object.is_staff,
        'teachers':teachers
    }
    return render(request,'teacher/faculty_table.html',context)

def faculty_by_subject(request,id):
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    sid=id
    current_subject=Subject.objects.filter(id=sid).first()
    teachers=Teacher.objects.filter(assigned_subject=current_subject)
    context={
        'teacher_is_staff':current_teacher.is_staff,
        'teachers':teachers
    }
    return render(request,'teacher/faculty_table.html',context)