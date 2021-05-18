from django.shortcuts import render
from course.models import Course
from subject.models import Subject
from student.models import Student
from teacher.models import Teacher
from .models import Sem
from django.contrib.auth.decorators import login_required


def students_in_sem(request,id):
    semid=id
    curr_sem=Sem.objects.filter(id=semid).first()
    students=Student.objects.filter(sem=curr_sem)
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    if current_student is not None:
        context={
            'is_student': current_student.is_student,
            'sem':curr_sem,
            'students':students,
        }
        return render(request,'sem/sem_error.html',context)
    elif current_teacher is not None:
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'sem':curr_sem,
            'students':students,
        }
        return render(request,'sem/student_insem.html',context)
    else:
        return render(request,'sem/sem_error.html')

def sems_in_course_faculty(request,id):
    cid=id
    user_id=request.user.id
    current_course=Course.objects.filter(id=cid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    sems=Sem.objects.filter(course=current_course)
    if current_teacher is not None:
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'sems':sems,
        }
        return render(request,'sem/sems_in_course_faculty.html',context)
    elif current_student is not None:
        context={
            'is_student':current_student.is_student,
            'sems':sems,
        }
        return render(request,'sem/sem_in_course_faculty.html',context)
    else:
        return render(request,'sem/sem_error.html')
