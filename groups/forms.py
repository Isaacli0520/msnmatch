from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name','group_intro','group_type','picture')
        labels = {
            'group_name':'Group Name',
        	'group_intro' : 'Introduction',
            'group_type':'Group Type',
        }
       	help_texts = {
        }
