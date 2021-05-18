from django.shortcuts import render, get_object_or_404, redirect
from .forms import AnswerCreateForm,MarksForm,AnswerUpdateForm,ReasonForm
from assignment.models import Assignment
from .models import Answer,Reason
from student.models import Student
from student.views import sendemail_rejected,sendemail_accepted
from teacher.models import Teacher
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from lms1.settings import EMAIL_HOST_USER
# Create your views here.
'''Saatvik
Roll No: 18030121073
BCA Sem 6
'''

def sendemail_new_answer(latest_answer):
    maillist=[]
    assignment=latest_answer.assignment
    author=assignment.author
    maillist.append(author.teacher.email)
    subject="Reply to your assignment. Answer created on: "+latest_answer.date_posted.strftime("%d %m %Y")
    message="You have a new answer reply to "+assignment.title+" please go to your dashboard and check it out"
    recepient=maillist[0]
    send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)

def create_answer(request,id):
    user_id=request.user.id
    aid=id
    current_student=Student.objects.filter(student=user_id).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_assignment=Assignment.objects.all().filter(id=aid)
    answer=Answer.objects.filter(assignment=current_assignment.first()).filter(author=current_student).first()
    if current_assignment.first().currently_active == False:
        return render(request,'answer/expired_assignment_error.html')

    if current_student is None or current_teacher is not None:
        return render(request,'answer/answer_error.html')
    if answer is not None:
        context={
            'answer':answer,
            'is_student':current_student.is_student,
        }
        return render(request,'answer/resubmission_error.html',context)
    if request.method=='POST':
        form=AnswerCreateForm(request.POST,request.FILES)
        user_id=request.user.id
        current_student=Student.objects.all().filter(student=user_id).first()
        current_assignment=Assignment.objects.all().filter(id=aid)
        form.instance.author=current_student
        form.instance.assignment=current_assignment.first()
        form.instance.course=current_student.assigned_course
        form.instance.subject=current_assignment.first().subject
        if form.is_valid():
            form.save()
            temp=Answer.objects.last()
            temp.title=request.POST['title']
            temp.save()
            answers_list=Answer.objects.all().filter(assignment=aid)
            context={
                'answers':answers_list,
                'is_student':current_student.is_student
            }
            messages.success(request,f'Answer Created Successfully') #display message after sucessful creation of answer
            latest_answer=Answer.objects.all().last() #get latest answer created
            sendemail_new_answer(latest_answer) #sendemail to teacher when answer is created
            return render(request,'answer/answers_list.html',context)
        else:
            return render(request,'answer/answer_submission_error.html')
    else:
        form=AnswerCreateForm()
        return render(request,'answer/submit_form.html',{'form':form,'is_student':current_student.is_student})

def loadpendinganswers(request,id): #pending answer by assignment
    aid=id
    user_id=request.user.id
    current_assignment=Assignment.objects.filter(id=aid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    student_answers=Answer.objects.filter(assignment=current_assignment).filter(status='PD')
    if current_teacher != current_assignment.author:
        context={
            'student_answers':student_answers,
            'teacher_is_staff':current_teacher.is_staff,
            'object':current_assignment,
            }
        return render(request,'answer/view_error.html',context)
    context={
        'status':'PD',
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        'object':current_assignment,
        }
    return render(request,'answer/status_answers.html',context)


def all_pending_student_answers(request,id): #load pending answer by student
    sid=id
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_teacher is not None:
        student=Student.objects.filter(id=sid).first()
        student_answers=Answer.objects.filter(author=student).filter(status='PD')
        context={
        'status':'PD',
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'answer/status_answers.html',context)
    else:
        student_answers=Answer.objects.filter(author=current_student).filter(status='PD')
        if student_answers.first().author == current_student:
            context={
                'status':'PD',
                'student_answers':student_answers,
                'is_student':current_student.is_student,
            }
            return render(request,'answer/status_answers.html',context)
        else:
            context={
                'is_student':current_student.is_student,
                'teacher_is_staff':current_teacher.is_staff,
            }
            return render(request,'answer/view_error.html',context)


def loadrejectedanswers(request,id): #loads rejected answer by assignment
    aid=id
    user_id=request.user.id
    current_assignment=Assignment.objects.filter(id=aid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    student_answers=Answer.objects.filter(assignment=current_assignment).filter(status='RJ')
    if current_teacher != current_assignment.author:
        context={
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        'object':current_assignment,
        }
        return render(request,'answer/view_error.html',context)
    context={
        'status':'RJ',
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        'object':current_assignment,
        }
    return render(request,'answer/status_answers.html',context)


def all_rejected_student_answers(request,id): #loads rejected answers by student
    sid=id
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_teacher is not None:
        student=Student.objects.filter(id=sid).first()
        student_answers=Answer.objects.filter(author=student).filter(status='RJ')
        context={
        'status':'RJ',
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'answer/status_answers.html',context)
    else:
        student_answers=Answer.objects.filter(author=current_student).filter(status='RJ')
        if student_answers.first().author == current_student:
            context={
                'status':'RJ',
                'student_answers':student_answers,
                'is_student':current_student.is_student,
            }
            return render(request,'answer/status_answers.html',context)
        else:
            context={
                'is_student':current_student.is_student,
                'teacher_is_staff':current_teacher.is_staff,
            }
            return render(request,'answer/view_error.html',context)



def loadacceptedanswers(request,id):
    aid=id
    user_id=request.user.id
    current_assignment=Assignment.objects.filter(id=aid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_student=Student.objects.filter(student=user_id).first()
    student_answers=Answer.objects.filter(assignment=current_assignment).filter(status='AC')
    if current_teacher != current_assignment.author:
        context={
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        'object':current_assignment,
        }
        return render(request,'answer/view_error.html',context)
    context={
        'status':'AC',
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        'object':current_assignment,
        }
    return render(request,'answer/status_answers.html',context)


def all_accepted_student_answers(request,id):
    sid=id
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_teacher is not None:
        student=Student.objects.filter(id=sid).first()
        student_answers=Answer.objects.filter(author=student).filter(status='AC')
        context={
        'status':'AC',
        'student_answers':student_answers,
        'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'answer/status_answers.html',context)
    else:
        student_answers=Answer.objects.filter(author=current_student).filter(status='AC')
        if student_answers.first().author == current_student:
            context={
                'status':'AC',
                'student_answers':student_answers,
                'is_student':current_student.is_student,
            }
            return render(request,'answer/status_answers.html',context)
        else:
            context={
                'is_student':current_student.is_student,
                'teacher_is_staff':current_teacher.is_staff,
            }
            return render(request,'answer/view_error.html',context)

def loadstudentanswers(request):
    user_id=request.user.id
    object=Student.objects.filter(id=user_id)
    currentstudent=object.first()
    answer_list=Answer.objects.filter(author=currentstudent)
    return render(request,'answer/answers_list.html',{'is_student':currentstudent.is_student})

def loadassignmentanswers(request,id):
    aid=id
    current_assignment=Assignment.objects.filter(id=aid).first()
    answers=Answer.objects.filter(assignment=current_assignment).order_by('-date_posted')
    object=Teacher.objects.filter(teacher=request.user.id).first()
    object2=Student.objects.filter(student=request.user.id).first()

    if object is not None:
        context={
            'answers':answers,
            'teacher_is_staff':object.is_staff,
            'teacher':object,
            'assignment':current_assignment,
        }
    elif object2 is not None:
        context={
            'answers':answers,
            'is_student':object2.is_student,
            'assignment':current_assignment,
        }
    return render(request,'answer/assignment_answers_list.html',context)

def accept_answer_func(id):
    aid=id
    current_answer=Answer.objects.filter(id=aid).first()
    current_teacher=current_answer.assignment.author
    if current_teacher == current_answer.assignment.author:
        current_answer.status='AC'
        current_answer.save()
        print(current_answer.status)
        context={
            'answer':current_answer,
            'teacher':current_teacher,
            'teacher_is_staff':current_teacher.is_staff,
        }
    else:
        pass

def accept_answer(request,id):
    tid=id
    current_answer=Answer.objects.filter(id=tid).first()
    user_id=request.user.id
    current_faculty=Teacher.objects.filter(teacher=user_id).first()
    current_student=current_answer.author
    student_answers_list=Answer.objects.filter(author=current_student)
    reason=Reason.objects.filter(answer=current_answer).first()
    if current_answer.status == 'AC':
        context={
            'answer':current_answer,
            'teacher':current_faculty,
            'teacher_is_staff':current_faculty.is_staff,
        }
        return render(request,'answer/already_accepted.html',context)
    if reason is not None:
        return render(request,'answer/resubmit_error_reason_accepted.html')
    if current_faculty is None:
        context={
            'current_student':current_student.is_student,
        }
        return render(request,'answer/m_error.html',context)
    if current_faculty != current_answer.assignment.author:
        print("Breakpoint2")
        context={
            'teacher_is_staff':current_faculty.is_staff,
            'teacher':current_faculty,
        }
        return render(request,'answer/m_error.html',context)
    m_form=MarksForm()
    r_form=ReasonForm()
    total_marks=0
    total_score=0
    for student_answer in student_answers_list:
        total_score+=student_answer.marks
        total_marks+=student_answer.assignment.assignment_marks
    current_answer.author.marks=total_score
    current_answer.author.save()
    context={
        'current_answer':current_answer,
        'm_form':m_form,
        'r_form':r_form,
        'teacher_is_staff':current_faculty.is_staff,
        'teacher':current_faculty,
    }
    if request.method=='POST':
        m_form=MarksForm(request.POST,instance=current_answer)
        r_form=ReasonForm(request.POST)
        r_form.instance.answer=current_answer
        current_answer.marks=m_form.instance.marks
        if m_form.is_valid() and r_form.is_valid():
            m_form.save()
            current_student.assignment_accepted+=1
            current_student.save()
            r_form.save()
            accept_answer_func(current_answer.id)
        context={
            'current_answer':current_answer,
            'm_form':m_form,
            'r_form':r_form,
            'teacher_is_staff':current_faculty.is_staff,
            'teacher':current_faculty,
        }
        messages.success(request,f'Marks Updated Successfully')
        sendemail_accepted(current_answer)
        return render(request,'answer/answers_list.html',context)
    return render(request,'answer/marks_form.html',context)


def reject_answer_confirm(request,id):
    aid=id
    user_id=request.user.id
    current_answer=Answer.objects.filter(id=aid).first()
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    if current_teacher == current_answer.assignment.author:
        context={
            'teacher':current_teacher,
            'teacher_is_staff':current_teacher.is_staff,
            'answer':current_answer,
        }
        return render(request,'answer/reject_answer_confirm.html',context)
    else:
        context={
            'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'answer/reject_error.html',context)



def reject_answer(id):
    aid=id
    current_answer=Answer.objects.filter(id=aid).first()
    current_teacher=current_answer.assignment.author
    if current_teacher == current_answer.assignment.author:
        current_answer.status='RJ'
        current_answer.save()
        context={
            'answer':current_answer,
            'teacher':current_teacher,
            'teacher_is_staff':current_teacher.is_staff,
        }
    else:
        pass


def reject_answer_form(request,id):
    aid=id
    user_id=request.user.id
    current_teacher=Teacher.objects.filter(teacher=user_id).first()
    current_answer=Answer.objects.filter(id=aid).first()
    reason=Reason.objects.filter(answer=current_answer).first()
    if current_answer.status == 'RJ':
        context={
            'answer':current_answer,
            'teacher':current_teacher,
            'teacher_is_staff':current_teacher.is_staff,
        }
        return render(request,'answer/already_rejected.html',context)
    if reason is not None:
        return render(request,'answer/resubmit_error_reason_rejected.html')
    if current_teacher != current_answer.assignment.author:
        context={
            'teacher_is_staff':current_teacher.is_staff,
            'teacher':current_teacher,
        }
        return render(request,'answer/reject_error.html',context)
    else:
        r_form=ReasonForm()
        if request.method == 'POST':
            r_form=ReasonForm(request.POST)
            r_form.instance.answer=current_answer
            if r_form.is_valid():
                r_form.save()
                reject_answer(current_answer.id)
                context={
                    'answer':current_answer,
                    'teacher_is_staff':current_teacher.is_staff,
                    'teacher':current_teacher,
                }
                messages.success(request,f'Answer Rejected Successfully')
                sendemail_rejected(current_answer)
                return render(request,'answer/answer_detail.html',context)
        else:
            context={
                'r_form':r_form,
                'teacher_is_staff':current_teacher.is_staff,
                'teacher':current_teacher,
                'answer':current_answer,
            }
            return render(request,'answer/reject_form.html',context)

def answer_by_faculty_dashboard(request,id):
    sid=id
    current_student=Student.objects.filter(id=sid).first()
    student_answers_list=Answer.objects.filter(author=current_student)
    user_id=request.user.id
    object=Teacher.objects.filter(teacher=user_id).first()
    total_marks=0
    total_score=0
    for student_answer in student_answers_list:
        total_score+=student_answer.marks
        total_marks+=student_answer.assignment.assignment_marks
    current_student.marks=total_score
    current_student.save()
    context={
        'teacher_is_staff':object.is_staff,
        'student':current_student,
        'student_answer':student_answers_list,
        'total_score':total_score,
        'total_marks':total_marks,
    }
    return render(request,'answer/answers_by_faculty_dashboard.html',context)

def answer_by_student(request,id):
    sid=id
    user_id=request.user.id
    current_student=Student.objects.filter(student=user_id).first()
    student_answers_list=Answer.objects.filter(author=current_student).order_by('-date_posted')
    object=Teacher.objects.filter(teacher=user_id).first()
    if current_student != Student.objects.filter(student=user_id).first():
        context={
            'student':current_student,
            'is_student':current_student.is_student,
        }
    total_marks=0
    total_score=0
    for student_answer in student_answers_list:
        total_score+=student_answer.marks
        total_marks+=student_answer.assignment.assignment_marks
    current_student.marks=total_score
    current_student.save()
    context={
            'student':current_student,
            'is_student':current_student.is_student,
            'student_answer':student_answers_list,
            'total_score':total_score,
            'total_marks':total_marks,
        }
    return render(request,'answer/answers_by_student_table.html',context)

'''def answerdetail(request,id):
    aid=id
    answers=Answer.objects.filter(id=aid)
    object=Teacher.objects.filter(teacher=request.user.id).first()
    object2=Student.objects.filter(student=request.user.id).first()
    if object is not None:
        context={
            'answers':answers,
            'teacher_is_staff':object.is_staff,
                }
    elif object2 is not None:
        context={
            'answers':answers,
            'is_student':object2.is_student,
                }
    return render(request,'answer/answers_list.html',context)'''

def answer_detail(request,id):
    aid=id
    answer=Answer.objects.filter(id=aid).first()
    student=Student.objects.filter(student=request.user.id).first()
    object=Teacher.objects.filter(teacher=request.user.id).first()
    current_reason=Reason.objects.filter(answer=answer).first()
    if object is not None:
        context={
            'teacher_is_staff':object.is_staff,
            'answer':answer,
            'teacher':object,
            'reason':current_reason,
        }
        return render(request,'answer/answer_detail.html',context)
    else:
        if student == answer.author:
            context={
                'current_student':student,
                'is_student':student.is_student,
                'answer':answer,
                'reason':current_reason,
            }
            return render(request,'answer/answer_detail.html',context)
        else:
            context={
                'current_student':student,
                'is_student':student.is_student,
                'answer':answer,
            }
            return render(request,'answer/view_error.html',context)

def sendemail_update_answer(latest_answer):
    maillist=[]
    assignment=latest_answer.assignment
    author=assignment.author
    maillist.append(author.teacher.email)
    subject="Answer named "+latest_answer.title+" has been Updated "
    message="Answer created on "+latest_answer.date_posted.strftime("%d %m %Y")+" has been updated by the student"
    recepient=maillist[0]
    send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)


def update_answer(request,id):
    aid=id
    user_id=request.user.id
    current_answer=Answer.objects.filter(id=aid).first()
    current_student=Student.objects.filter(student=user_id).first()
    if current_answer.author==current_student:
        context={
            'student':current_student,
            'answer':current_answer,
            'is_student':current_student.is_student,
        }
        if request.method == 'POST':
            u_form=AnswerUpdateForm(request.POST,request.FILES,instance=current_answer)
            if u_form.is_valid():
                u_form.save()
                temp=current_answer
                temp.title=request.POST['title']
                temp.save()
                sendemail_update_answer(current_answer)
                messages.success(request,f'Answer Updated Successfully')
                return render(request,'answer/answer_detail.html',context)
            else:
                return render(request,'answer/answer_submission_error.html')
        u_form=AnswerUpdateForm(instance=current_answer)
        context={
            'is_student':current_student.is_student,
            'student':current_student,
            'u_form':u_form,
            'answer':current_answer,
        }
        return render(request,'answer/update_answer.html',context)
    else:
        context={
            'student':current_student,
            'answer':current_answer,
            'is_student':current_student.is_student,
        }
        return render(request,'answer/update_error_answer.html',context)

def delete_answer_confirm(request,id):
    aid=id
    user_id=request.user.id
    current_answer=Answer.objects.filter(id=aid).first()
    current_student=Student.objects.filter(student=user_id).first()
    context={
            'student':current_student,
            'is_student':current_student.is_student,
            'answer':current_answer,
        }
    if current_answer.author == current_student:
        context={
            'student':current_student,
            'is_student':current_student.is_student,
            'answer':current_answer,
        }
        return render(request,'answer/delete_answer_confirm.html',context)
    else:
        return render(request,'answer/delete_error.html',context)


def delete_answer(request,id):
    aid=id
    user_id=request.user.id
    current_answer=Answer.objects.filter(id=aid).first()
    current_student=Student.objects.filter(student=user_id).first()
    Answer.objects.filter(id=aid).delete()
    context={
        'student':current_student,
        'answer':current_answer,
        'is_student':current_student.is_student,
    }
    return render(request,'answer/delete_answer_done.html',context)