from django.db import models
from django.contrib.auth.models import User
from course.models import Course
from subject.models import Subject

# Create your models here.
class Teacher(models.Model):
    teacher=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='teacher_profile_pics')
    assigned_course=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    assigned_subject=models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    is_staff=models.BooleanField(default=True)
    qualification=models.CharField(max_length=255,null=True,default=None)
    
    def __str__(self):
        return f'{self.teacher.username} teacher Profile'