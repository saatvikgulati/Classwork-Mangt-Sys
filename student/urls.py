from django.urls import path
from .import views
urlpatterns = [
    path('students-table/',views.students_table,name='students-table'),
    path('students-in-course/<int:id>/',views.students_in_course,name='course-students'),
    path('students-in-subjects/<int:id>/',views.students_in_subject,name='subject-students'),
    path('student-dashboard/',views.student_dashboard,name='student-dashboard'),
    path('student-profile/',views.student_profiles,name='student-profiles'),
    path('my_profile/',views.my_profile,name='my_profile'),
]
