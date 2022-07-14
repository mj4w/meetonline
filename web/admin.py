from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
#extending fields
 
class InformationAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','gender']
    search_fields = ['name']
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Region)

admin.site.register(Religion)
# admin.site.register(Information,InformationAdmin)
admin.site.register(Gender)
admin.site.register(Hobby)

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)
admin.site.register(Status)