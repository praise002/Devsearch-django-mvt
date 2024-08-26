from django.shortcuts import render
from django.views import View
from apps.accounts.mixins import LoginRequiredMixin
from apps.accounts.forms import UserEditForm
from .forms import SkillFormSet, ProfileEditForm
from .models import Skill, Profile
from django.db.models import Q
import sweetify

class EditView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                    'profiles/edit.html',
                    {'user_form': user_form,
                     'profile_form': profile_form})
        
    def post(self, request):
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST,
                                 files=request.FILES)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            sweetify.toast(request, 'Profile updated successfully')
        else:
            sweetify.error(request, 'Error updating your profile')
        return render(request,
                    'profiles/edit.html',
                    {'user_form': user_form,
                     'profile_form': profile_form})

class SkillEditView(LoginRequiredMixin, View):
    def get(self, request):
        # Fetching all skills related to the user's profile
        formset = SkillFormSet(queryset=Skill.objects.filter(user=request.user.profile))
        return render(request,
                      'profiles/skill_edit.html',
                      {'formset': formset})
        
    def post(self, request):
        formset = SkillFormSet(data=request.POST,
                               queryset=Skill.objects.filter(user=request.user.profile))
        if formset.is_valid():
            formset.save()
            sweetify.toast(request, 'Skills updated successfully')
        else:
            sweetify.error(request, 'Error updating skills')
        return render(request,
                      'profiles/skill_edit.html',
                      {'formset': formset})
        
class ProfileDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user__username=kwargs['username'])
        skills_with_description = profile.skills.filter(~Q(description=""))
        skills_without_description = profile.skills.filter(description="")
        context = {
            'profile': profile,
            'skills_with_description': skills_with_description,
            'skills_without_description': skills_without_description,
        }
        return render(request, 'profiles/profile.html', context)