from django.db import models
# Create your models here.
class Course(models.Model):
    course_list=[('BCA','BCA'),('BBA_IT','BBA_IT'),('BSCIT','BSCIT')]
    name=models.CharField(max_length=255,default = 'BCA')
    no_of_students = models.IntegerField(default=0,null=True)
    '''course_list=[('BCA','BCA'),('BBA_IT','BBA_IT'),('BSCIT','BSCIT')]
    name=models.CharField(max_length=255,choices=course_list)
    faculty_assigned=models.ForeignKey(Teacher,on_delete=models.CASCADE)'''
    def __str__(self):
        return f'{self.name}'

