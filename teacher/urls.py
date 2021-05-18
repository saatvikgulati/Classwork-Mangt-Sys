from django.urls import path
from . import views
urlpatterns=[
    #path('register/',views.Teacherregister,name='teacher-register'),
    path('dashboard/',views.facultydashboard,name='faculty-dashboard'),
    path('faculty-table/',views.faculty_table,name='faculty-table'),
    path('faculty-table-by-course/<int:id>/',views.faculty_by_course,name='faculty-table-by-course'),
    path('faculty-table-by-subject/<int:id>/',views.faculty_by_subject,name='faculty-table-by-subject'),
]