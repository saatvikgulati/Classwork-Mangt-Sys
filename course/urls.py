from django.urls import path
from . import views

urlpatterns=[
    path('course_detail_faculty/<int:id>/',views.course_detail_faculty,name='course-detail-faculty'),
    path('course_detail_student/<int:id>/',views.course_detail_student,name='course-detail-student'),
    path('course_table/',views.coursetable_faculty,name='course-table'),
]