from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from .managers import CustomUserManager
import uuid

def slugify_two_fields(self):
    return f"{self.first_name}-{self.last_name}"

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    username = AutoSlugField(
        _("Username"), populate_from=slugify_two_fields, unique=True, always_update=True
    )
    email = models.EmailField(_("Email address"), unique=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    user_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = CustomUserManager()
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['username']),
        ]
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def __str__(self):
        return self.full_name


