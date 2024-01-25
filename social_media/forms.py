from django import forms
from django.contrib.auth.models import User

from .models import UserPost, Profile, PostComment


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


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('profile', 'post', 'comment',)
        widgets = {
            'profile': forms.HiddenInput(),
            'post': forms.HiddenInput(),
            'comment': forms.Textarea(),
        }
        labels = {
            'comment': 'Add a comment',
        }
