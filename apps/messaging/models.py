from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.profiles.models import Profile
from apps.common.models import BaseModel

class Message(BaseModel):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='messages')
    name = models.CharField(_("Name"), max_length=200, blank=True) 
    email = models.EmailField(_("Email"), max_length=200)
    subject = models.CharField(_("Subject"), max_length=200)
    body = models.TextField(_("Body"))
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ["is_read", "-created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
