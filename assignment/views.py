from django.shortcuts import render
from django.views.generic import ListView
from teacher.models import Teacher
from student.models import Student
from answer.models import Answer
from .models import Assignment
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import AssignmentCreateForm
from django.core.mail import send_mail
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from lms1.settings import EMAIL_HOST_USER
# Create your views here.
'''Saatvik
Roll No: 18030121073
BCA Sem 6
'''

def home(request):
    assignment_list=Assignment.objects.all().order_by('-date_posted')
    page=request.GET.get('page',1)
    paginator=Paginator(assignment_list,2)
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    context={
        'title':'Saatvik',
        'posts':posts
        }
    if request.method=='GET':
        object=Teacher.objects.filter(teacher=request.user.id).first()
        object2=Student.objects.filter(student=request.user.id).first()
        if object is not None:
            context={
                    'title':'Saatvik',
                    'posts':posts,
                    'teacher_is_staff':object.is_staff,
                    }
        elif object2 is not None:
            context={
                    'title':'Saatvik',
                    'posts':posts,
                    'is_student':object2.is_student,
                    
                    }
    else:
        context={
        'title':'Saatvik',
        'posts':posts
        }
    return render(request,'assignment/home.html',context)


def about(request):
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    context={
            'title':'About',
        }
    if current_teacher is not None:
        context={
            'title':'About',
            'teacher_is_staff':current_teacher.is_staff,
            'teacher':current_teacher,
        }
    elif current_student is not None:
        context={
            'title':'About',
            'is_student':current_student.is_student,
            'student':current_student,
        }
    return render(request,'assignment/about.html',context)

def teacher_assignment(request):
    user_id=request.user.id
    object=Teacher.objects.filter(teacher=user_id).first()
    assignment_list=Assignment.objects.filter(author=object)
    context={
        'teacher_is_staff':object.is_staff,
        'assignments':assignment_list,
    }
    return render(request,'assignment/teacher_assignment.html',context)


def all_assignment(request):
    context={
        'assignments':Assignment.objects.filter(author=object)
    }
    return render(request,'assignment/all_assignment.html',context)

def sendemail_assignment(latest_assignment): #to be used in create_assignment
    mailist=[]
    course=latest_assignment.course
    student_list=Student.objects.filter(assigned_course=course)
    for student in student_list:
        mailist.append(student.student.email)
    subject="New Assignment Posted on "+latest_assignment.date_posted.strftime("%d %m %Y")
    message="You have a new assignment named \'"+latest_assignment.title+"\' please go to your dashboard and check it out"
    for recepient in mailist:
        send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)


def create_assignment(request):
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_student is not None or current_teacher is None:
        return render(request,'assignment/assignment_error.html') #error handling
    if request.method=='POST':
        form=AssignmentCreateForm(request.POST,request.FILES)
        user_id=request.user.id
        object=Teacher.objects.filter(teacher=user_id).first()
        form.instance.author=object
       
        if form.is_valid():
            form.save()
            assignment=Assignment.objects.all()
            temp=assignment.last()
            temp.title=request.POST['title']
            temp.save()
            context={
            'title':'Saatvik',
            'posts':Assignment.objects.all(),
            'teacher_is_staff':object.is_staff,
            }
            messages.success(request,f'Assignment Created Successfully') #display message after successful creation of assignment
            latest_assignment=Assignment.objects.all().last() #get latest assignment created
            sendemail_assignment(latest_assignment) #sendemail to students when assignment is created
            return render(request,'assignment/assignment_list.html',context)
    else:
        form =AssignmentCreateForm()
    object=Teacher.objects.filter(teacher=user_id).first()
    return render(request,'assignment/assignment_form.html',{'form':form,'teacher_is_staff':object.is_staff})

def assignment_detail(request,id):
    aid=id
    currentassignment=Assignment.objects.filter(id=aid).first()
    current_teacher=Teacher.objects.filter(teacher=request.user.id).first()
    current_student=Student.objects.filter(student=request.user.id).first()
    context={
        'title':'Saatvik',
        'posts':Assignment.objects.all(),
        'object':currentassignment,
    }
    if current_teacher is not None:
        context={
            'title':'Saatvik',
            'posts':Assignment.objects.all(),
            'object':currentassignment,
            'teacher':current_teacher,
            'teacher_is_staff':current_teacher.is_staff,
        }
    elif current_student is not None:
        currentassignment.views+=1 #when a student views assignment
        currentassignment.save()
        context={
            'title':'Saatvik',
            'posts':Assignment.objects.all(),
            'object':currentassignment,
            'student':current_student,
            'is_student':current_student.is_student,
        }
    return render(request,'assignment/assignment_detail.html',context)

def loadteachers(request):
    teacher_list=Teacher.objects.all()
    user_id=request.user.id
    object=Teacher.objects.filter(teacher=user_id)
    context={
        'teachers':teacher_list,
        'teacher_is_staff':request.user.id
    }
    return render(request,'assignment/all_faculty.html',context)

def assignment_status(assignment_list):
    for assignment in assignment_list:
        if timezone.now() > assignment.expires_on:
            if assignment.currently_active!=False:
                assignment.currently_active=False
                assignment.save()

def faculty_assignment_table(request):
    user_id=request.user.id
    object=Teacher.objects.filter(teacher=user_id)
    current_teacher=object.first()
    assignment_list=Assignment.objects.filter(author=current_teacher).order_by('-date_posted')
    assignment_status(assignment_list)
    page=request.GET.get('page',1)
    paginator=Paginator(assignment_list,3)
    try:
        assignments=paginator.page(page)
    except PageNotAnInteger:
        assignments=paginator.page(1)
    except EmptyPage:
        assignments=paginator.page(paginator.num_pages)
    context={
        'assignments':assignments,
        'teacher_is_staff':current_teacher.is_staff,
    }
    return render(request,'assignment/assignment_table.html',context)

def student_assignment_table(request):
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    assignment_list=Assignment.objects.filter(course=current_student.assigned_course).order_by('-date_posted')
    assignment_status(assignment_list)
    page=request.GET.get('page',1)
    paginator=Paginator(assignment_list,3)
    try:
        assignments=paginator.page(page)
    except PageNotAnInteger:
        assignments=paginator.page(1)
    except EmptyPage:
        assignments=paginator.page(paginator.num_pages)
    context={
        'assignments':assignments,
        'is_student':current_student.is_student,
    }
    return render(request,'assignment/student_assignment_table.html',context)

def sendemail_assignment_update(latest_assignment): #to be used in create_assignment
    mailist=[]
    course=latest_assignment.course
    student_list=Student.objects.filter(assigned_course=course)
    for student in student_list:
        mailist.append(student.student.email)
    subject="Assignment has been updated "
    message="Your assignment named \'"+latest_assignment.title+"\' has been updated "
    for recepient in mailist:
        send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)


def update_assignment(request,id):
    aid=id
    current_assignment=Assignment.objects.get(id=aid)
    user_id=request.user.id
    current_user=Teacher.objects.filter(teacher=user_id).first()
    if current_assignment.author==current_user:
        if request.method=="POST":
            u_form=AssignmentCreateForm(request.POST,request.FILES,instance=current_assignment)
            if u_form.is_valid():
                u_form.save()
                temp=current_assignment
                temp.title=request.POST['title']
                temp.save()
                context={
                    'teacher_is_staff':current_user.is_staff,
                    'form':u_form,
                    'object':current_assignment,
                }
                sendemail_assignment_update(current_assignment)
                messages.success(request,f'Assignment Updated Successfully')
                return render(request,'assignment/assignment_detail.html',context)
        else:
            u_form=AssignmentCreateForm(instance=current_assignment)
            context={
                    'teacher_is_staff':current_user.is_staff,
                    'form':u_form,
                    'object':current_assignment,
                }
            return render(request,'assignment/assignment_form.html',context)
    else:
        context={
            'teacher_is_staff':current_user.is_staff,
            'object':current_assignment,
        }
        return render(request,'assignment/update_error_assignment.html',context)


def delete_assignment_confirm(request,id):
    aid=id
    user_id=request.user.id
    current_assignment=Assignment.objects.filter(id=aid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_teacher is None:
        return render(request,'assignment/delete_error.html')
    if current_assignment.author==current_teacher:
        context={
            'teacher':current_teacher,
            'object':current_assignment,
            'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'assignment/delete_assignment_confirm.html',context)
    else:
        return render(request,'assignment/delete_error.html')

def sendemail_assignment_delete(latest_assignment): #to be used in create_assignment
    mailist=[]
    course=latest_assignment.course
    student_list=Student.objects.filter(assigned_course=course)
    for student in student_list:
        mailist.append(student.student.email)
    subject="Assignment Deleted!!! Due on: "+latest_assignment.expires_on.strftime("%d %m %Y")
    message="Your assignment has been deleted named \' "+latest_assignment.title+" \' "
    for recepient in mailist:
        send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)


def delete_assignment(request,id):
    aid=id
    user_id=request.user.id
    current_assignment=Assignment.objects.filter(id=aid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    Assignment.objects.filter(id=aid).delete()
    context={
        'teacher':current_teacher,
        'object':current_assignment,
        'teacher_is_staff':current_teacher.is_staff,
    }
    sendemail_assignment_delete(current_assignment)
    return render(request,'assignment/delete_assignment_done.html',context)