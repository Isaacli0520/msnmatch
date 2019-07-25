from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
  first_name = models.CharField(max_length=255, default="Null")
  last_name = models.CharField(max_length=255, default="Null")
  def __str__(self):
    return self.first_name + " " + self.last_name;

class Department(models.Model):
  name = models.CharField(max_length=255, default="")
  school = models.CharField(max_length=255, default="")

def get_department():
  Department.objects.get_or_create(id=1)
  return 1

class Course(models.Model):
  users = models.ManyToManyField(User, through='CourseUser')
  instructors = models.ManyToManyField(Instructor, through='CourseInstructor')
  number = models.CharField(max_length = 100,default="0")
  mnemonic = models.CharField(max_length=30, blank=True)
  units = models.CharField(max_length=30, default='0')
  title = models.CharField(max_length=500, blank=True)
  description = models.TextField(blank=True)
  prerequisite = models.CharField(max_length = 1000, blank=True)
  type=models.CharField(max_length=100, blank=True)
  rating = models.FloatField(null=True, blank=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE, default=get_department)

  def __str__(self):
    return self.mnemonic + str(self.number)


class CourseInstructor(models.Model):
  instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  semester = models.CharField(max_length=100, default="Null")
  topic = models.CharField(max_length=500, blank=True)


class CourseUser(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default = 1)
  take = models.CharField(max_length=255,default="Null")
  course_instructor = models.ForeignKey(CourseInstructor, on_delete=models.CASCADE, default = 1)
  text = models.CharField(max_length=2000, blank=True)
  rating_instructor = models.FloatField(null=True, blank=True)
  rating_course = models.FloatField(null=True, blank=True)
  section = models.CharField(max_length=255, blank=True)


# 'ClassNumber', 'Mnemonic', 'Number', 'Section', 'Type', 'Units',
#  'Instructor(s)', 'Days', 'Room', 'Title', 'Topic', 'Status', 
#  'Enrollment', 'EnrollmentLimit', 'Waitlist', 'CombinedWith', 'Description'