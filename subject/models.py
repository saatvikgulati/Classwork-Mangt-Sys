from django.db import models
from course.models import Course
# from sem.models import Sem

class Subject(models.Model):
    # subject_list =[('VAVR','Verification and validtion tehcniques'),('DWDM','Datawarehousing and data mining '),('DTSC1','Introduction to data science '),('COA','Computer Organisation and Architecture'),('Mup','Micro Controller and Processor'),('WebT','Web Technologies'),('ST','Statistics')]
    subject_name =models.CharField(max_length=25,default='VAVR')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default=None)
    lectures = models.IntegerField()
    duration = models.IntegerField()
    # sem = models.ForeignKey(Sem,on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.subject_name}'