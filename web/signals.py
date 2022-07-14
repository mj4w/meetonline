from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User
from django.conf import settings
#signals is to give signal to our deploy user or variable that we create    
# decorator with @
@receiver (post_save, sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver (post_save, sender=User)
def saved_profile(sender,instance, **kwargs): # kwargs is to except initial arguments end of the function
    instance.profile.save()