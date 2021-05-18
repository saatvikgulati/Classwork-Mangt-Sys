from django.db import models
from assignment.models import Assignment
from django.utils import timezone
from student.models import Student
from course.models import Course
from subject.models import Subject
from django.urls import reverse
from .validators import validate_file_extension
# Create your models here.

class Answer(models.Model):
    title=models.CharField(max_length=50)
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    author=models.ForeignKey(Student,on_delete=models.CASCADE)
    pdf=models.FileField(upload_to='answers',validators=[validate_file_extension])
    content=models.TextField(default='Content Here')
    date_posted=models.DateTimeField(default=timezone.now)
    status_choice=[('PD','Pending'),('AC','Accepted'),('RJ','Rejected')]
    status=models.CharField(max_length=20,choices=status_choice,default='PD')
    marks=models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self): #the reverse method will return the data as string
        return reverse('student-answer-list',kwargs={'id':self.id})
    def delete(self,*args,**kwargs):
        self.pdf.delete()
        super().delete(*args,**kwargs)
    def save(self, *args, **kwargs):
        try:
            this = Answer.objects.filter(id=self.id)
            if this.pdf != self.pdf:
                this.pdf.delete()
        except: pass
        super(Answer, self).save(*args, **kwargs)

class Reason(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    reason=models.TextField(default='Reason',null=True)
    date_posted=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.answer.title