from django.db import models
from course.models import Course
from subject.models import Subject


class Sem(models.Model):
    course = models.ManyToManyField(Course)
    subject = models.ManyToManyField(Subject)
    # sem_list = [(1,1),(2,2),(3,3),(4,4),(5,5),(),(),(),()]
    sem_no = models.IntegerField(default=1,null = False)
    # sem_type_choices = [('Even','Even'),('Odd','Odd')]
    # sem_type = models.CharField(max_length = 10, choices = sem_type_choices)
    # semname = models.CharField(max_length =5,default = 'One')
    
    def __str__(self):
        return f'{self.sem_no}'
    def save(self,*args, **kwargs):
        super(Sem, self).save(*args, **kwargs)
    
    