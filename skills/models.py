from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
  users = models.ManyToManyField(User, through='SkillRelation')
  intro = models.CharField(max_length=255, blank=True)
  name = models.CharField(max_length=30, blank=True)
  type = models.CharField(max_length=40, blank=True)

  def __str__(self):
    return self.name

class SkillRelation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE)