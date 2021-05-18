from django.db import models
from teacher.models import Teacher
from course.models import Course
from subject.models import Subject
from .validators import validate_file_extension
from django.utils import timezone
# Create your models here.
class Notes(models.Model):
    author=models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    description=models.TextField(default="Content Here")
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    attachement=models.FileField(upload_to='notes',validators=[validate_file_extension])
    upload_date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.description
    def delete(self,*args,**kwargs):
        self.attachement.delete()
        super().delete(*args,**kwargs)
    def save(self, *args, **kwargs):
        try:
            this = Notes.objects.filter(id=self.id)
            if this.attachment != self.attachement:
                this.attachement.delete()
        except: pass
        super(Notes, self).save(*args, **kwargs)