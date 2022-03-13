from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import UserProfile, Consultation, AuthCode
from chat.models import create_room


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance, auth_code=AuthCode.objects.create())
        profile.save()


@receiver(post_save, sender=Consultation)
def push_message(sender, instance: Consultation, **kwargs):
    if kwargs['created']:
        create_room(instance.insigator_id, instance.consultant_id, instance.id)
