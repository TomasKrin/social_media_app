from PIL import Image
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    profile_views = models.IntegerField(default=0)
    profile_pic = models.ImageField('profile_pic', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'img'])],
                                    default='profile_pics/default.jpg', upload_to='profile_pics')

    def get_user_id(self):
        return self.user.id

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_posts_count(self):
        return self.posts.all().count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        profile_pic = Image.open(self.profile_pic.path)
        original_width, original_height = profile_pic.size

        if profile_pic.width > profile_pic.height:
            desired_height = 500
            desired_width = 700
        else:
            desired_height = 500
            desired_width = 500

        aspect_ratio = original_width / original_height
        new_height = desired_height
        new_width = int(aspect_ratio * new_height)

        if new_width > desired_width:
            new_width = desired_width
            new_height = int(new_width / aspect_ratio)
        profile_pic = profile_pic.resize((new_width, new_height), Image.LANCZOS)
        if profile_pic.mode == 'RGBA':
            profile_pic = profile_pic.convert('RGB')
        profile_pic.save(self.profile_pic.path, quality=95)

    def __str__(self):
        return self.display_name


STATUS_CHOICE = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} -> {self.receiver} - {self.status}'


class UserPost(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    post = models.TextField(verbose_name='Post')
    liked = models.ManyToManyField(Profile, related_name='likes', blank=True)
    img = models.ImageField('Image', upload_to='post_images', null=True, blank=True)

    def num_likes(self):
        return self.liked.all().count()

    def format_date(self):
        return self.date_posted.strftime('%Y-%m-%d %H:%M')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.img:
            img = Image.open(self.img.path)
            max_height = 300

            if img.height > max_height:
                aspect_ratio = img.width / img.height
                new_width = int(max_height * aspect_ratio)
                new_size = (new_width, max_height)
                img = img.resize(new_size, Image.LANCZOS)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(self.img.path, format='JPEG', quality=95)

    def __str__(self):
        return f'{self.date_posted} {self.profile} {self.post}'


class PostComment(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    liked_comment = models.ManyToManyField(Profile, related_name='commentlikes', blank=True)
    comment = models.TextField(verbose_name='Comment')

    def get_post_id(self):
        return self.post.id

    get_post_id.short_description = 'Post'

    def __str__(self):
        return f'{self.date_posted} {self.profile} {self.comment}'


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class PostLike(models.Model):
    like_added = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)

    def __str__(self):
        return f'{self.profile} {self.post.post} {self.value}'


class CommentLike(models.Model):
    like_added = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)

    def __str__(self):
        return f'{self.profile} {self.comment.comment} {self.value}'
