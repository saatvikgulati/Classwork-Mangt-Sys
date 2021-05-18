"""lms1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from teacher.models import Teacher
from student.models import Student
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('assignment.urls')),
    path('teacher/',include('teacher.urls')),
    path('answers/',include('answer.urls')),
    path('student/',include('student.urls')),
    path('course/',include('course.urls')),
    path('subject/',include('subject.urls')),
    path('notes/',include('notes.urls')),
    path('sem/',include('sem.urls')),
    path('faculty-login/',auth_views.LoginView.as_view(template_name='teacher/teacherlogin.html'),name='faculty-login'),
    path('faculty-logout/',auth_views.LogoutView.as_view(template_name='teacher/teacherlogout.html'),name='faculty-logout'),
    
    path('faculty-password-reset/',auth_views.PasswordResetView.as_view(template_name='teacher/password_reset.html'),name='password_reset_faculty'),
    path('faculty-password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='teacher/password_reset_done.html'),name='password_reset_done'),
    path('faculty-password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='teacher/password_reset_confirm.html'),name='password_reset_confirm'),
    path('faculty-reset-done/',auth_views.PasswordResetCompleteView.as_view(template_name='teacher/password_reset_complete.html'),name='password_reset_complete'),
    path('faculty-password-change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='teacher/password_change_done.html',extra_context={'teacher_is_staff':Teacher.objects.filter().first().is_staff}),name='password_change_done'),
    path('faculty-password-change/',auth_views.PasswordChangeView.as_view(template_name='teacher/password_change.html',extra_context={'teacher_is_staff':Teacher.objects.filter().first().is_staff}),name='password_change_faculty'),
    
    path('student-password-reset/',auth_views.PasswordResetView.as_view(template_name='student/password_reset.html'),name='password_reset_student'),
    path('student-password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='student/password_reset_done.html'),name='password_reset_done'),
    path('student-password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='teacher/password_reset_confirm.html'),name='password_reset_confirm'),
    path('student-reset-done/',auth_views.PasswordResetCompleteView.as_view(template_name='student/password_reset_complete.html'),name='password_reset_complete'),
    path('student-password-change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='student/password_change_done.html',extra_context={'is_student':Student.objects.filter().first().is_student}),name='password_change_done'),
    path('student-password-change/',auth_views.PasswordChangeView.as_view(template_name='student/password_change.html',extra_context={'is_student':Student.objects.filter().first().is_student}),name='password_change_student'),
    
    path('student-login/',auth_views.LoginView.as_view(template_name='student/studentlogin.html'),name='student-login'),
    path('student-logout/',auth_views.LogoutView.as_view(template_name='student/studentlogout.html'),name='student-logout'),
    path('guest-logout/',auth_views.LogoutView.as_view(template_name='assignment/guestlogout.html'),name='guest-logout'),
]

if settings.DEBUG:
    urlpatterns+=[

    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
