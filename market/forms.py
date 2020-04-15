from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'price', 'description', 'category', 'image', 'pickup','condition','delivery', 'user')

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'price', 'description', 'category', 'image', 'pickup','condition','delivery', 'id')
