from django.urls import path
from . import views

urlpatterns=[
    path('subject-detail/<int:id>/',views.subject_detail,name='subject-detail'),
    path('subjects-table-student/',views.subjects_table_student,name='subject-table-student'),
]