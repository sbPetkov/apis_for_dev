from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from api.profiles_api.models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.email = instance.username
        profile.save()
    else:
        instance.profile.email = instance.username
        instance.profile.save()
