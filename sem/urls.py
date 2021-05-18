from django.urls import path
from . import views
urlpatterns=[
    path('student-in-sem/<int:id>/',views.students_in_sem,name='students-in-sem'),
    path('sems-in-course/<int:id>/',views.sems_in_course_faculty,name='sems-in-course'),
]