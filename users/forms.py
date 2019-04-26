from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location','bio','year','sex', 'major', 'major_two', 'minor', 'birth_date','picture')
        labels = {
        	'birth_date' : 'Birth Date',
        }
       	help_texts = {
            'birth_date': 'Format: mm/dd/yyyy',
        }
