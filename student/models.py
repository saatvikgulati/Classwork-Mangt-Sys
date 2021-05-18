from django.db import models
from django.contrib.auth.models import User
from course.models import Course
from subject.models import Subject
from sem.models import Sem
from .validators import validate_file_extension

# Create your models here.
class Student(models.Model):
    student=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpeg',upload_to='student_profile_pics',validators=[validate_file_extension])
    course_list=[('BCA','BCA'),('BBA_IT','BBA_IT'),('BSCIT','BSCIT')]
    assigned_course=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    subject_list=[('VAVR','Verification and Validation'),('DWDM','Data Warehousing and Mining'),('DTSC1','Introduction to Data Science')]
    assigned_subject=models.ManyToManyField(Subject)
    year=models.CharField(max_length=60,default=None,null=True)
    branch=models.CharField(max_length=60,default=None,null=True)
    assignment_accepted=models.IntegerField(default=0)
    marks=models.IntegerField(default=0)
    is_student=models.BooleanField(default=True)
    sem = models.ForeignKey(Sem,on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.student.username} Profile'
    def save(self, *args, **kwargs):
        
        try:
            this=Student.objects.filter(id=self.id)
            if this.MyImageFieldName != self.MyImageFieldName:
                this.MyImageFieldName.delete()
        except:
            pass
        super(Student, self).save(*args, **kwargs)

    
    
        