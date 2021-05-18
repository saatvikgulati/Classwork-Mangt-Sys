from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='assignment-home'),
    path('about-us/',views.about,name='about-us'),
    path('assignment/',views.teacher_assignment,name='teacher-assignment'),
    path('assignment/create/',views.create_assignment,name='assignment-create'),
    path('assignment-detail/<int:id>/',views.assignment_detail,name='assignment-detail'),
    path('faculty-assignment-table/',views.faculty_assignment_table,name='faculty-assignment-table'),
    path('student-assignment-table/',views.student_assignment_table,name='student-assignment-table'),
    path('assignment-update/<int:id>/',views.update_assignment,name='update-assignment'),
    path('assignment-delete-confirm/<int:id>/',views.delete_assignment_confirm,name='delete-assignment-confirm'),
    path('assignment-delete/<int:id>/',views.delete_assignment,name='delete-assignment'),
]