# Generated by Django 4.2.9 on 2024-01-25 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0009_postcomment_liked_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpost',
            name='liked',
        ),
    ]
