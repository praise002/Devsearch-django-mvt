from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,)
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import password_validation
from django.template.loader import render_to_string

from .models import User
from .senders import EmailThread
from .validators import validate_name

class RegistrationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("Password Mismatch."),
    }
    first_name = forms.CharField(
        validators=[validate_name],
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "e.g. Dennis", "class": "input input--text"})
    )
    last_name = forms.CharField(
        validators=[validate_name],
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "e.g. Ivanov", "class": "input input--text"})
    )
    email = forms.EmailField(
        error_messages={"unique": _("Email already registered")},
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "e.g. user@domain.com", "class": "input input--email"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••", "class": "input input--password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••", "class": "input input--password"}),
    )

    
    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "email", 
            "password1", 
            "password2",
            ]
    
    def _post_clean(self):
        super(RegistrationForm, self)._post_clean()
        password1 = self.cleaned_data["password1"]
        if len(password1) < 8:
            self.add_error("password1", "Password too short")

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address...", "class": "input input--text"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••", "class": "input input--password"}),
    )
    
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"placeholder": "e.g. user@domain.com", "autocomplete": "email", "class": "input input--email"}),
    )
    
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        user = User.objects.filter(email=to_email).first()
        if user:
            context["name"] = user.full_name
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            context["name"]
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        EmailThread(email_message).start()


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "input input--password"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "input input--password"}
        ),
    )
    
class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        validators=[validate_name],
        max_length=50,
        widget=forms.TextInput(attrs={"class": "input input--text"})
    )
    last_name = forms.CharField(
        validators=[validate_name],
        max_length=50,
        widget=forms.TextInput(attrs={"class": "input input--text"})
    )
    
    class Meta:
        model = User
        fields = [ 
            "photo", 
            ] #TODO: FIX LATER, TRANSFER TO PROFILE APP
