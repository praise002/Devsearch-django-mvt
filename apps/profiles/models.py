from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
import uuid

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey('Profile', related_name='skills', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    class Meta:
        unique_together = ('user', 'name')
        
    def __str__(self):
        return self.name

class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Social Links
    social_github = models.URLField(max_length=200, blank=True)
    social_stackoverflow = models.URLField(max_length=200, blank=True)
    social_twitter = models.URLField(max_length=200, blank=True)
    social_linkedin = models.URLField(max_length=200, blank=True)
    social_website = models.URLField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.user.full_name}"

