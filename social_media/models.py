from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50)
    profile_views = models.IntegerField(default=0)
    profile_pic = models.ImageField('profile_pic', default='profile_pics/default.png', upload_to='profile_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile_pic = Image.open(self.profile_pic.path)
        if profile_pic.height > 200 or profile_pic.width > 200:
            new_size = (200, 200)
            profile_pic.thumbnail(new_size)
            profile_pic.save(self.profile_pic.path)

    def __str__(self):
        return self.display_name


class UserPost(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.TextField(verbose_name='Post')
    img = models.ImageField('Image', upload_to='post_images', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Call the "real" save() method.
        super().save(*args, **kwargs)

        # Open the image using Pillow.
        img = Image.open(self.img.path)

        # Define the maximum height.
        max_height = 300

        # Check if the image height is greater than the maximum height.
        if img.height > max_height:
            # Calculate the new width maintaining the aspect ratio.
            aspect_ratio = img.width / img.height
            new_width = int(max_height * aspect_ratio)
            new_size = (new_width, max_height)

            # Perform the resizing operation.
            img = img.resize(new_size, Image.LANCZOS)

            # If the image mode is RGBA, convert it to RGB before saving as JPEG.
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Save the resized image back to the path.
            img.save(self.img.path, format='JPEG', quality=95)
        # If the image is smaller than max_height, do nothing.

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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)


class CommentLike(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
