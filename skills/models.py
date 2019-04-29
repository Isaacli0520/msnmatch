from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
  skill_users = models.ManyToManyField(User, through='SkillRelation')
  skill_intro = models.CharField(max_length=255, blank=True)
  skill_name = models.CharField(max_length=30, blank=True)
  skill_type = models.CharField(max_length=40, blank=True)

  def __str__(self):
    return self.skill_name

class SkillRelation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE)