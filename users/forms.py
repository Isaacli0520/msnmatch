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
        fields = ('location','bio','graduate_year','sex', 'major', 'major_two', 'minor', 'birth_date','wechat','picture', 'video')
        labels = {
            'sex':'Gender',
        	'birth_date' : 'Birth Date',
            'wechat':'WeChat ID',
        }
       	help_texts = {
            'birth_date': 'Format: mm/dd/yyyy',
        }

class ProfileNewForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','graduate_year','sex', 'major', 'major_two', 'minor','wechat','picture','video','rm_bio','rm_schedule')