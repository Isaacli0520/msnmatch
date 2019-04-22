from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
  course_users = models.ManyToManyField(User, through='Relation')
  course_number = models.CharField(max_length=30, blank=True)
  course_name = models.CharField(max_length=255, blank=True)

class Relation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  take = models.CharField(max_length=255,default="null")
