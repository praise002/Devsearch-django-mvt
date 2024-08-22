from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from .forms import RegistrationForm
from .mixins import LoginRequiredMixin, LogoutRequiredMixin
from .models import User
from .senders import SendEmail, email_verification_generate_token
from .forms import (
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    LoginForm,
    RegistrationForm,
    UserEditForm
)

import sweetify

class RegisterView(LogoutRequiredMixin, View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 
                      'accounts/signup.html',
                      {'form': form})
        
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            SendEmail.verification(request, user)
            request.session['verification_email'] = user.email
            return render(request, 
                      'accounts/email_verification_sent.html',
                      {'form': form})
            
        return render(request, 
                      'accounts/signup.html',
                      {'form': form})

class LoginView(LogoutRequiredMixin, View):
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "accounts/login.html", context)
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            password = cd['password']
            user = authenticate(request, 
                                username=email, 
                                password=password) # verify the identity of a user
            
            if not user:
                sweetify.error(self.request, 'Invalid Credentials')
                return redirect('accounts:login')
            if not user.is_active:
                sweetify.error(self.request, 'Disabled account')
            if not user.is_email_verified:
                request.session['verification_email'] = email  # store email in session if user is not verified
                SendEmail.verification(request, user)
                return render(request, 
                      'accounts/email_verification_sent.html',
                      {'form': form})
                
            # passes all above test, login user
            login(request, user)
            return redirect('gallery:home')
        
        context = {"form": form}
        return render(request, "accounts/login.html", context)

class VerifyEmail(LogoutRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs["uidb64"]
        token = kwargs["token"]
        user_id = kwargs["user_id"]
        
        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            sweetify.error(self.request, 'You entered an invalid link')
            return redirect(reverse('accounts:login')) 
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except Exception:
            user = None
            
        request.session['verification_email'] = (
            user_obj.email
        )  # Restoring email to session (incase request was made from a different client)
        
        if user:
            if user.id != user_obj.id:
                print(user.id != user_obj.id)
                sweetify.error(self.request, 'You entered an invalid link')
                return redirect(reverse('accounts:login'))
            
            if email_verification_generate_token.check_token(user, token):
                user.is_email_verified = True
                user.save()
                sweetify.toast(self.request, 'Verification successful!')
                request.session["verification_email"] = None
                SendEmail.welcome(request, user)
                return redirect(reverse('accounts:login'))
                
        return render(
            request,
            "accounts/email_verification_failed.html",
            {"email": user_obj.email},
        )

class ResendVerificationEmail(LogoutRequiredMixin, View):
    def get(self, request) :
        email = request.session.get("verification_email")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            sweetify.error(self.request, 'Not allowed')
            return redirect(reverse('accounts:login'))
        
        if user.is_email_verified:
            sweetify.info(self.request, 'Email address already verified!')
            request.session["verification_email"] = None
            return redirect(reverse('accounts:login'))
        
        SendEmail.verification(request, user)
        sweetify.toast(self.request, 'Email Sent')
        return render(request, 
                      'accounts/email_verification_sent.html')

class CustomPasswordResetView(LogoutRequiredMixin, PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset_form.html"

class CustomPasswordResetConfirmView(LogoutRequiredMixin, PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "accounts/password_reset_confirm.html"

class CustomPasswordResetDoneView(LogoutRequiredMixin, PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetCompleteView(LogoutRequiredMixin, PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
    
class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs): # if it doesnt work change to get
        logout(request)
        return redirect('accounts:login')
        # return redirect('gallery:home')

class LogoutAllDevices(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        request.session.flush()  # Clear all session data
        return redirect('gallery:home')  # Redirect to the home page or any other desired page

class EditView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request,
                    'accounts/edit.html',
                    {'form': form})
        
    def post(self, request):
        form = UserEditForm(instance=request.user,
                                 data=request.POST,
                                 files=request.FILES)
        if form.is_valid():
            form.save()
            sweetify.toast(request, 'Profile updated successfully')
        else:
            sweetify.error(request, 'Error updating your profile')
            
        return render(request,
                    'accounts/edit.html',
                    {'form': form})