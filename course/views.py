from django.shortcuts import render
from .models import Course
from teacher.models import Teacher
from student.models import Student
from django.contrib.auth.decorators import login_required
# Create your views here.
'''Saatvik
Roll No: 18030121073
BCA Sem 6
'''

def course_detail_faculty(request,id):
    cid=id
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_course=Course.objects.filter(id=cid).first()
    students_list=Student.objects.filter(assigned_course=current_course)
    no_of_students = students_list.count()
    context={
        'teachers':current_teacher,
        'current_course':current_course,
        'teacher_is_staff':current_teacher.is_staff,
        'no_of_students':no_of_students
    }

    
    students_list=Student.objects.filter(assigned_course=current_course)
    

    return render(request,'course/course_detail_faculty.html',context)


def course_detail_student(request,id):
    cid=id
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_course=Course.objects.filter(id=cid).first()
    students_list=Student.objects.filter(assigned_course=current_course)
    
    context={
        'student':current_student,
        'current_course':current_course,
        'is_student':current_student.is_student,
    }
    return render(request,'course/course_detail_student.html',context)


def coursetable_faculty(request):
    user_id = request.user.id
    courses = Course.objects.all()
    current_teacher = Teacher.objects.filter(teacher = user_id).first()
    
    # if current_teacher is None:
    #     context={
    #     'student':current_student,
    #     'current_course':current_course,
    #     'is_student':current_student.is_student,
    #     }
    #     # return render(request,'course/error.html')
    
    context = {
        'teacher':current_teacher,
        'courses':courses,
        'teacher_is_staff':current_teacher.is_staff,
    }
    
    return render(request,'course/course_table.html',context)

