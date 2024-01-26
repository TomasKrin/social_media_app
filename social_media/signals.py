from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User, Relationship


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
      Signal to create a Profile instance automatically when a new User instance is created.
    """
    if created:
        Profile.objects.create(user=instance, display_name=instance.first_name)


@receiver(post_save, sender=Relationship)
def add_to_friends(sender, instance, created, **kwargs):
    """
    Signal to add users as friends in their respective profiles when a Relationship instance
    with status 'accepted' is created or updated.
    """
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()
