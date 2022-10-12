from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import DateField
from traitlets import default

# Create your models here.
class Record(models.Model):
    id=models.AutoField
    roll_no=models.CharField(max_length=20)
    course=models.CharField(default="",max_length=20)
    time=models.CharField(max_length=30)
    date=models.DateField(auto_now=True)
    present=models.BooleanField(default=False)

class CourseStudent(models.Model):
    id=models.AutoField
    roll_no=models.CharField(max_length=20)
    course=models.CharField(default="",max_length=20)
    

