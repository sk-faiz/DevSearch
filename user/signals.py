from django.contrib.auth.models import User
# Create your models here.
from .models import *
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user, name=user.first_name , user_name=user.username, email=user.email)

def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.user_name
        user.email = profile.email
        user.save()

def profileDelete(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(profileDelete, sender=Profile)