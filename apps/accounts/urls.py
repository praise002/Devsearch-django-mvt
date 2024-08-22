from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout-all-devices/', views.LogoutAllDevices.as_view(), name='logout_all_devices'),
    
    # Email verification
     path('verify-email/<uidb64>/<token>/<user_id>/', 
          views.VerifyEmail.as_view(), name='verify_email'),
     path('resend-verification-email/', 
          views.ResendVerificationEmail.as_view(), 
          name='resend_verification_email'),

     # change password urls
     path('password-change/',
          auth_views.PasswordChangeView.as_view(
               template_name='accounts/password_change_form.html',
               success_url = reverse_lazy("accounts:password_change_done"),
          ),
          name='password_change'),
     path('password-change/done/',
          auth_views.PasswordChangeDoneView.as_view(
               template_name='accounts/password_change_done.html',
          ),
          name='password_change_done'),

     # reset password urls
     path(
          'reset-password/',
          views.CustomPasswordResetView.as_view(
               email_template_name='accounts/password_reset_html_email.html',
               html_email_template_name='accounts/password_reset_html_email.html',
               success_url = reverse_lazy("accounts:password_reset_done")
          ),
          name='reset_password',
     ),
          
     path('reset-password/done/',
          views.CustomPasswordResetDoneView.as_view(),
          name='password_reset_done'),
     path('reset-password/<uidb64>/<token>/',
          views.CustomPasswordResetConfirmView.as_view(
               success_url = reverse_lazy("accounts:password_reset_complete"),
          ),
          name='password_reset_confirm'),
     path('reset-password/complete/',
          views.CustomPasswordResetCompleteView.as_view(),
          name='password_reset_complete'),
     

     path('edit/', views.EditView.as_view(), name="edit"),
]
