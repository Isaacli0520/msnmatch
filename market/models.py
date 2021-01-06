from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image
from io import BytesIO
import uuid

condition_choices = [
    ('new','New'),
    ('slightlyused','Slightly Used'),
    ('used','Used'),
    ('dysfunctional','Dysfunctional')
]
category_choices = [
    ('electronics', 'Electronics'),
    ('textbooks', 'Textbooks'),
    ('schoolsupplies', 'School Supplies'),
    ('pets', 'Pets'),
    ('clothing', 'Clothing'),
    ('housing', 'Housing'),
    ('furniture', 'Furniture'),
    ('miscellaneous', 'Miscellaneous')
]

class Item(models.Model):
    name = models.CharField(max_length=35, default='')
    price = models.DecimalField(decimal_places=2, max_digits=10, default='0.0')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=200, choices=condition_choices, default='Used')
    category = models.CharField(max_length=25, choices=category_choices, default='Miscellaneous')
    pickup = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    description = models.CharField(max_length=350, default='')
    image = models.ImageField(upload_to="msn/market/image/",blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # address = models.CharField(max_length=200, default='University of Virginia')
    
    def save(self, *args, **kwargs):
        try:
            this = Item.objects.filter(pk=self.pk).first()
            if (this and self.image and this.image != self.image) or (not this and self.image):
                self.image.name = str(uuid.uuid4()) + self.image.name[self.image.name.rfind('.'):]
        except: pass

        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return "Item: " + self.name