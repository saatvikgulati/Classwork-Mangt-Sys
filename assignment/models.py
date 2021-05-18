from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import timedelta
from teacher.models import Teacher
from course.models import Course
from subject.models import Subject
from django.urls import reverse
from .validators import validate_file_extension
# Create your models here.
class Assignment(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    content=models.TextField()
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    date_posted=models.DateTimeField(default=timezone.now)
    expires_on=models.DateTimeField(default=((timezone.now()+timedelta(days=2))))
    currently_active=models.BooleanField(default=True)
    pdf=models.FileField(upload_to='assignments', validators=[validate_file_extension])
    assignment_marks=models.IntegerField(default=10)
    views=models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.title
    def get_absolute_url(self): #the reverse method will return the data as string
        return reverse('assignment-detail',kwargs={'id':self.id})
    def delete(self,*args,**kwargs):
        self.pdf.delete()
        super().delete(*args,**kwargs)
    def save(self, *args, **kwargs):
        try:
            this = Assignment.objects.filter(id=self.id)
            if this.pdf != self.pdf:
                this.pdf.delete()
        except: pass
        super(Assignment, self).save(*args, **kwargs)
        if self.expires_on < timezone.now():
            self.currently_active=False
            super().save()
        super().save()