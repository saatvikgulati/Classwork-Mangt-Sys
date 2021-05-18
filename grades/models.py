from django.db import models
from answer.models import Answer
from student.models import Student
from teacher.models import Teacher
from assignment.models import Assignment
from answer.models import Answer
# Create your models here.
class Grade(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE,default=None)
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE,default=None)
    question_marks=models.IntegerField(default=10)
    given_marks=models.IntegerField(default=0)
    def __str__(self):
        return self.student.username