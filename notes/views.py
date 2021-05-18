from django.shortcuts import render
from .models import Notes
from teacher.models import Teacher
from student.models import Student
from subject.models import Subject
from .forms import NoteCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from lms1.settings import EMAIL_HOST_USER
# Create your views here.
'''Saatvik
Roll No: 18030121073
BCA Sem 6
'''

def faculty_notes(request):
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    #current_student=Student.objects.filter(student=user_id).first()
    if current_teacher is None:
        return render(request,'notes/notes_unauthorized_access.html')
    else:
        notes=Notes.objects.filter(author=current_teacher)
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'notes':notes,
        }
        return render(request,'notes/faculty_notes.html',context)

def sendemail_notes_create(latest_notes): #to be used in deleting notes
    mailist=[]
    subject=latest_notes.subject
    student_list=Student.objects.filter(assigned_subject=subject)
    for student in student_list:
        mailist.append(student.student.email)
    subject="Notes Created!!! Created on: "+latest_notes.upload_date.strftime("%d %m %Y")
    message="Your notes has been created named \' "+latest_notes.description+" \' "
    for recepient in mailist:
        send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)

def create_notes(request):
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_teacher is None:
        return render(request,'notes/notes_unauthorized_access.html')
    if request.method == "POST":
        n_form=NoteCreationForm(request.POST,request.FILES)
        if n_form.is_valid():
            notes=Notes.objects.filter(author=current_teacher)
            n_form.instance.author=current_teacher
            n_form.instance.course=current_teacher.assigned_course
            n_form.instance.subject=current_teacher.assigned_subject
            n_form.save()
            context={
                'teacher_is_staff':current_teacher.is_staff,
                'notes':notes,
            }
            messages.success(request,f'Notes Created Successfully')
            latest_notes=Notes.objects.all().last() #get latest notes created
            sendemail_notes_create(latest_notes) #send email to students when notes are created
            return render(request,'notes/faculty_notes.html',context)
        else:
            return render(request,'notes/notes_unauthorized_access.html')
    else:
        n_form=NoteCreationForm()
        context={
            'n_form':n_form,
            'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'notes/create_notes_form.html',context)

def subject_table_student_notes(request):
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    if current_student is None:
        return render(request,'notes/notes_unauthorized_access.html')
    else:
        student_subjects=current_student.assigned_subject.all()
        context={
            'is_student':current_student.is_student,
            'subjects':student_subjects,
        }
        return render(request,'notes/subject_table_student_notes.html',context)

def student_notes(request,id):
    sid=id
    user_id=request.user.id
    current_subject=Subject.objects.filter(id=sid).first()
    current_student=Student.objects.filter(student=user_id).first()
    if current_student is None:
        return render(request,'notes/notes_unauthorized_access.html')
    else:
        notes=Notes.objects.filter(subject=current_subject)
        context={
            'is_student':current_student.is_student,
            'notes':notes,
        }
        return render(request,'notes/student_notes.html',context)

def sendemail_notes_update(latest_notes): #to be used in deleting notes
    mailist=[]
    subject=latest_notes.subject
    student_list=Student.objects.filter(assigned_subject=subject)
    for student in student_list:
        mailist.append(student.student.email)
    subject="Notes Updated!!! Created on: "+latest_notes.upload_date.strftime("%d %m %Y")
    message="Your notes has been updated named \' "+latest_notes.description+" \' "
    for recepient in mailist:
        send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)

def update_notes(request,id):
    nid=id
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_note=Notes.objects.filter(id=nid).first()
    if current_teacher is None:
        return render(request,'notes/notes_unauthorized_access.html')
    if current_teacher == current_note.author:
        notes=Notes.objects.filter(author=current_teacher)
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'notes':notes,
        }
        if request.method == "POST":
            n_form=NoteCreationForm(request.POST,request.FILES,instance=current_note)
            if n_form.is_valid():
                n_form.save()
                messages.success(request,f'Notes Updated Successfully')
                sendemail_notes_update(current_note)
                return render(request,'notes/faculty_notes.html',context)
            else:
                return render(request,'notes/notes_unauthorized_access.html')
        else:
            n_form=NoteCreationForm(instance=current_note)
            context={
                'teacher_is_staff':current_teacher.is_staff,
                'n_form':n_form,
            }
            return render(request,'notes/create_notes_form.html',context)
    else:
        context={
            'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'notes/update_notes_error.html',context)

def delete_notes_confirm(request,id):
    nid=id
    user_id=request.user.id
    current_notes=Notes.objects.filter(id=nid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_teacher is None:
        return render(request,'notes/notes_unauthorized_access.html')
    if current_notes.author == current_teacher:
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'notes':current_notes,
        }
        return render(request,'notes/delete_notes_confirm.html',context)
    else:
        return render(request,'notes/delete_notes_error.html')

def sendemail_notes_delete(latest_notes): #to be used in deleting notes
    mailist=[]
    subject=latest_notes.subject
    student_list=Student.objects.filter(assigned_subject=subject)
    for student in student_list:
        mailist.append(student.student.email)
    subject="Notes Deleted!!! Created on: "+latest_notes.upload_date.strftime("%d %m %Y")
    message="Your notes has been deleted named \' "+latest_notes.description+" \' "
    for recepient in mailist:
        send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)

def delete_notes(request,id):
    nid=id
    user_id=request.user.id
    current_notes=Notes.objects.filter(id=nid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    Notes.objects.filter(id=nid).delete()
    context={
        'teacher_is_staff':current_teacher.is_staff,
        'notes':current_notes,
    }
    sendemail_notes_delete(current_notes)
    return render(request,'notes/delete_notes_done.html',context)
