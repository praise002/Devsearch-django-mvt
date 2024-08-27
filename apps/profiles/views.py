from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from apps.accounts.mixins import LoginRequiredMixin
from apps.accounts.forms import UserEditForm
from .forms import SkillForm, ProfileEditForm
from .models import Skill, Profile
from django.db.models import Q
import sweetify

class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        skills = profile.skills.all()
        
        context = {
            'profile': profile,
            'skills': skills,
        }
        return render(request, 'profiles/account.html', context)
    
class ProfileEditView(LoginRequiredMixin, View):
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
            # return redirect('')
        else:
            sweetify.error(request, 'Error updating your profile')
        return render(request,
                    'profiles/edit.html',
                    {'user_form': user_form,
                     'profile_form': profile_form})

class SkillCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = SkillForm()
        context = {'form': form}
        return render(request,
                      'profiles/skill_form.html',
                      context)
        
    def post(self, request, *args, **kwargs):
        form = SkillForm(request.POST)
            
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user.profile
            skill.save()
            sweetify.toast(request, 'Skill was added successfully!')
            # return redirect('')
        else:
            sweetify.error(request, 'Error adding skills')
            
        return render(request,
                      'profiles/skill_form.html',
                      {'form': form})

class SkillEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        skill = get_object_or_404(Skill, id=kwargs.get('id'), user=request.user.profile)
        form = SkillForm(instance=skill)
        context = {'form': form}
        return render(request,
                      'profiles/skill_form.html',
                      context)
    
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        skill = get_object_or_404(profile.skills, id=kwargs.get('id'))
        form = SkillForm(request.POST, instance=skill)
        
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user.profile
            skill.save()
            sweetify.toast(request, 'Skill was updated successfully!')
        else:
            sweetify.error(request, 'Error updating skill')
            
        context = {'form': form}
        return render(request,
                      'profiles/skill_form.html',
                      context)
        
class SkillDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        skill = get_object_or_404(profile.skills, id=kwargs.get('id'))
        context = {'skill': skill}
        return render(request, 'profiles/delete_template.html', context)
    
    def post(self, request, *args, **kwargs):
        skill = get_object_or_404(Skill, id=kwargs.get('id'), user=request.user.profile)
        skill.delete()
        sweetify.toast(request, 'Skill was deleted successfully')
        return redirect('profiles:account')
        
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