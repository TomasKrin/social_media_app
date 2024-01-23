# forms.py in your Django app

from django import forms
from .models import UserPost


class UserPostForm(forms.ModelForm):
    img = forms.ImageField(required=False, label='Image')

    class Meta:
        model = UserPost
        fields = ('profile', 'post', 'img',)
        widgets = {
            'profile': forms.HiddenInput(),
            'post': forms.Textarea(),
        }
