from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50)
    profile_views = models.IntegerField(default=0)
    profile_pic = models.ImageField('profile_pic', default='profile_pic/default.png', upload_to='profile_pics')

    def __str__(self):
        return self.display_name


class UserPost(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.TextField(verbose_name='Post')
    img = models.ImageField('Image', null=True, blank=True)

    def __str__(self):
        return f'{self.date_posted} {self.profile} {self.post}'


class PostComment(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comment')

    def get_post_id(self):
        return self.post.id

    get_post_id.short_description = 'Post'

    def __str__(self):
        return f'{self.date_posted} {self.profile} {self.comment}'


class PostLike(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class CommentLike(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
