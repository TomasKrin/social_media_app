# Generated by Django 4.2.9 on 2024-01-24 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0007_alter_userpost_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='social_media.userpost'),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='post_images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='social_media.profile'),
        ),
    ]
