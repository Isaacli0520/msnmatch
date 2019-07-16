from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
  name=models.CharField(max_length=255, default="Null")
  def __str__(self):
    return self.name

class Course(models.Model):
  users = models.ManyToManyField(User, through='CourseUser')
  instructors = models.ManyToManyField(Instructor, through='CourseInstructor')
  number = models.CharField(max_length = 100,default="0")
  mnemonic = models.CharField(max_length=30, blank=True)
  units = models.CharField(max_length=30, default='0')
  title = models.CharField(max_length=500, blank=True)
  topic = models.CharField(max_length=500, blank=True)
  description = models.TextField(blank=True)
  prerequisite = models.CharField(max_length = 1000, blank=True)
  type=models.CharField(max_length=100, blank=True)

  def __str__(self):
    return self.mnemonic + str(self.number)

class CourseUser(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  take = models.CharField(max_length=255,default="Null")

class CourseInstructor(models.Model):
  instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  semester = models.CharField(max_length=100, default="Null")


class Review(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  course_instructor = models.ForeignKey(CourseInstructor, on_delete=models.CASCADE)
  text = models.TextField(default="Null")

# 'ClassNumber', 'Mnemonic', 'Number', 'Section', 'Type', 'Units',
#  'Instructor(s)', 'Days', 'Room', 'Title', 'Topic', 'Status', 
#  'Enrollment', 'EnrollmentLimit', 'Waitlist', 'CombinedWith', 'Description'