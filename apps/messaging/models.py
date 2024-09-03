from django.db import models
from apps.profiles.models import Profile
import uuid

class Message(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='messages')
    name = models.CharField(max_length=200, blank=True) 
    email = models.EmailField(max_length=200, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ["is_read", "-created"]
        indexes = [
        models.Index(fields=["created"]),
        ]
