
from django.db import models

from datetime import datetime
import os,random
from django.utils.html import mark_safe

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings 

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager,AbstractUser
from django.utils import timezone
import uuid

class Gender(models.Model):
    gender = models.CharField(max_length=10)
    def __str__(self):
        return self.gender

class Hobby(models.Model):
    hobby = models.CharField(max_length=20)
    def __str__ (self):
        return self.hobby
class Status(models.Model):
    status = models.CharField(max_length=100)
    def __str__(self):
        return self.status
########################################### USER MODEL
class User(AbstractUser):
    name = models.CharField(max_length=200, null= True)
    last_name = models.CharField(max_length=200, null= True , verbose_name="Last Name")
    email = models.EmailField(unique=True,null=True)
    age = models.IntegerField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null = True)
    bio = models.TextField(null=True, max_length=1000)
    fb_url = models.CharField(max_length=255, blank=True)
    insta_url = models.CharField(max_length=255, blank=True)
    twitter_url = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(null=True)
    avatar = models.ImageField( default='avatar.png', upload_to='images')
   
    location = models.CharField(null=True, max_length=50)
    school = models.CharField(null=True, max_length=100)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    created_on =models.DateTimeField(default=timezone.now)
    hobby = models.ForeignKey(Hobby, on_delete=models.SET_NULL, null = True , blank=True, verbose_name= "Whats your hobby?")
    USERNAME_FIELDS = 'email'
    REQUIRED_FIELDS = []
######################################### CUSTOMIZATION



#post model
class Post(models.Model):
    # sharedpost 
    shared_body = models.TextField(blank=True, null=True)
    shared_on = models.DateTimeField(blank=True, null=True)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    post = models.TextField(blank=True,null=True)
    image = models.ManyToManyField('Image', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank = True, related_name='Likes')
    dislikes = models.ManyToManyField(User, blank= True, related_name="Dislikes")
    # to make organized
    class Meta:
        ordering = ['-created_on', '-shared_on']

#comment
class Comment(models.Model):
    comment = models.TextField()
    created_on=  models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True , related_name="comlikes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="comdislikes")

# Profile



    
def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)
class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=user_directory_path, null = True, blank = True)

    def __str__(self):
        return f'{self.user.username}'
class Religion(models.Model):
    religion = models.CharField(max_length=50)
    def __str__(self):
        return self.religion


class Region(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


#dms
class Notification(models.Model):
    #1 = like ,  2= COmment , 3 = Follow ,4 = message
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null= True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="+" , blank=True, null= True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    thread= models.ForeignKey('ThreadModel',on_delete=models.CASCADE , related_name="+", blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
class MessageModel (models.Model):
    thread = models.ForeignKey("ThreadModel",related_name="+", on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    body = models.CharField(max_length=1000, blank= True, null=True)
    image = models.ImageField(upload_to= 'upload/message_photos',blank= True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

class Follow(models.Model):
    is_follow = models.ManyToManyField(User, blank=True, related_name="is_follow")
    is_disfollow = models.ManyToManyField(User, blank=True, related_name="is_disfollow")

#multiple image post
class Image(models.Model):

    image = models.ImageField(upload_to = "uploads", null=True, default='avatar.png')
