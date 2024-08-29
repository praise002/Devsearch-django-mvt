from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# from django.forms import modelformset_factory
from .models import Profile, Skill

User = get_user_model()

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
                  "short_intro", "bio", "location",
                  "social_github", "social_stackoverflow",
                  "social_twitter", "social_linkedin",
                  ] 

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        
# extra=1 - number of empty forms to display initially
# SkillFormSet = modelformset_factory(Skill, fields=('name', 'description'), extra=1)