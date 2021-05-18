from django.urls import path
from .import views
urlpatterns=[
    path('submit-answer/<int:id>/',views.create_answer,name='submit-answer'),
    #path('answers-list/',views.answers_list,name='answer-list'),
    path('student-answers-list/',views.loadstudentanswers,name='student-answer-list'),
    path('assignment-answers-list/<int:id>/',views.loadassignmentanswers,name='assignment-answers-list'),
    path('marks-form/<int:id>/',views.accept_answer,name='marks-form'),
    path('answers-by-student/<int:id>/',views.answer_by_student,name='answers-by-student'),
    path('answer-detail/<int:id>/',views.answer_detail,name='answer-detail'),
    path('answers-by-faculty-dashboard/<int:id>/',views.answer_by_faculty_dashboard,name='answers-by-faculty-dashboard'),
    path('answer-update/<int:id>/',views.update_answer,name='answer-update'),
    path('answer-delete-confirm/<int:id>/',views.delete_answer_confirm,name='answer-delete-confirm'),
    path('answer-delete/<int:id>/',views.delete_answer,name='delete-answer'),
    path('status-answers-pending/<int:id>/',views.loadpendinganswers,name='pending-answer'),
    path('status-answers-rejected/<int:id>/',views.loadrejectedanswers,name='rejected-answer'),
    path('status-answer-accepted/<int:id>/',views.loadacceptedanswers,name='accepted-answer'),
    path('reject-answer-form/<int:id>/',views.reject_answer_form,name='reject-answer-form'),
    path('reject-answer-confirm/<int:id>/',views.reject_answer_confirm,name='reject-answer-confirm'),
    path('all-pending-student-answer/<int:id>/',views.all_pending_student_answers,name='pending-student-answer'),
    path('all-rejected-student-answer/<int:id>/',views.all_rejected_student_answers,name='reject-student-answer'),
    path('all-accepted-student-answer/<int:id>/',views.all_accepted_student_answers,name='accept-student-answer'),
    #path('reject-answer/<int:id>/',views.reject_answer,name='reject-answer'),
]