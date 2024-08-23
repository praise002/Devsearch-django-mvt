from django.shortcuts import render
from django.views import View
from apps.accounts.mixins import LoginRequiredMixin
from apps.accounts.forms import UserEditForm
from .forms import SkillFormSet, ProfileEditForm
import sweetify

class EditView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        formset = SkillFormSet(instance=request.user.profile)
        return render(request,
                    'profiles/edit.html',
                    {'user_form': user_form,
                     'profile_form': profile_form,
                     'formset': formset})
        
    def post(self, request):
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST,
                                 files=request.FILES)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        formset = SkillFormSet(instance=request.user.profile,
                                 data=request.POST)
        if user_form.is_valid() and profile_form.is_valid() and formset.is_valid():
            user_form.save()
            profile_form.save()
            formset.save()
            sweetify.toast(request, 'Profile updated successfully')
        else:
            sweetify.error(request, 'Error updating your profile')
            
        return render(request,
                    'profiles/edit.html',
                    {'user_form': user_form,
                     'profile_form': profile_form,
                     'formset': formset})
