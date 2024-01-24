# forms.py in your Django app

from django import forms
from django.contrib.auth.models import User

from .models import UserPost, Profile


class UserPostForm(forms.ModelForm):
    img = forms.ImageField(required=False, label='Image')

    class Meta:
        model = UserPost
        fields = ('profile', 'post', 'img',)
        widgets = {
            'profile': forms.HiddenInput(),
            'post': forms.Textarea(),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('display_name', 'profile_pic',)
