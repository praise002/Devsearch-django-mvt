from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel
from django.urls import reverse
import uuid

class Skill(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
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
    short_intro = models.CharField(_("Short Intro"), max_length=200, blank=True, null=True)
    bio = models.TextField(_("Bio"), blank=True)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    photo = models.ImageField(_("Photo"), upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    
    # Social Links
    social_github = models.URLField(_("Social Github"), max_length=200, blank=True)
    social_stackoverflow = models.URLField(_("Social Stackoverflow"), max_length=200, blank=True)
    social_twitter = models.URLField(_("Social Twitter"), max_length=200, blank=True)
    social_linkedin = models.URLField(_("Social LinkedIn"), max_length=200, blank=True)
    social_website = models.URLField(_("Social Website"), max_length=200, blank=True)
    
    # class Meta:
    #     indexes = [
    #         models.Index(fields=['short_intro']),
    #     ]  # TODO: MIGHT REMOVE LATER
    
    def __str__(self):
        return f"{self.user.full_name}"
    
    def get_absolute_url(self):
        return reverse('profiles:profile_detail', kwargs={'username': self.user.username})
    
    @property
    def image_url(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url

