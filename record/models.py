from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import DateField
from traitlets import default
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email_token=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)

# Create your models here.
class Record(models.Model):
    id=models.AutoField
    roll_no=models.CharField(max_length=20)
    course=models.CharField(default="",max_length=20)
    time=models.CharField(max_length=30)
    date=models.DateField()
    present=models.BooleanField(default=False)

class CourseStudent(models.Model):
    roll_no=models.CharField(max_length=20)
    course_1=models.CharField(default="",max_length=20)
    course_2=models.CharField(default="",max_length=20)
    course_d1=models.CharField(default="",max_length=20)
    course_d2=models.CharField(default="",max_length=20)
    course_o1=models.CharField(default="",max_length=20)
    course_o2=models.CharField(default="",max_length=20)
    

