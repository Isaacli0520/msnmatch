from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Slide(models.Model):
    name = models.CharField(max_length=255, default="Null")
    url = models.URLField(max_length=2500, default="Null")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "Slide: " + self.name