from django.contrib import admin
from .models import Skill, Profile
# class Profile(admin.ModelAdmin)

admin.site.register(Skill)
admin.site.register(Profile)
