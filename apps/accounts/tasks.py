from django.core.mail import EmailMessage
from apps.profiles.models import Profile
from celery import shared_task
from django.utils import timezone

from apps.projects.models import Review
from .models import User
from datetime import timedelta
from django.template.loader import render_to_string

def reminder_email(user): 
    subject = "Account Inactivity Reminder"
    context = {
        "name": user.full_name,
    }
    message = render_to_string("accounts/emails/account_inactivity.html", context)
    email_message = EmailMessage(subject=subject, body=message, to=[user.email])
    email_message.content_subtype = "html"
    email_message.send(fail_silently=False)
    
@shared_task
def send_reminder_emails():
    reminder_days = 7  # days before account deletion to send reminder
    inactive_days = 100  # days after which account will be deleted
    
    reminder_date = timezone.now() - timedelta(days=inactive_days + reminder_days)
    delete_date = timezone.now() - timedelta(days=inactive_days)
    
    # Find inactive users and send reminders
    inactive_users = User.objects.filter(last_login__lt=reminder_date)
    for user in inactive_users:
        # send reminder email
        reminder_email(user)
    
    # Delete users past the delete threshold
    users_to_delete = User.objects.filter(last_login__lt=delete_date)
    for user in users_to_delete:
        user.delete()

def weekly_email(profile, received_reviews): 
    subject = f"Weekly Update for {profile.user.full_name}"
    domain = "http://127.0.0.1:8000"
    context = {
        "name": profile.user.full_name,
        "received_reviews": received_reviews,
        "domain": domain,
    }
    message = render_to_string("accounts/emails/weekly_updates.html", context)
    email_message = EmailMessage(subject=subject, body=message, 
                                 to=[profile.user.email])
    email_message.content_subtype = "html" 
    email_message.send(fail_silently=False)  
        
@shared_task
def send_weekly_updates():
    one_week_ago = timezone.now() - timedelta(days=7)
    # today = timezone.now().date() 
    
    profiles = Profile.objects.all() #TODO: OPTIMIZE
    for profile in profiles:
        received_reviews = Review.objects.filter(project__owner=profile,
                                                 created__gte=one_week_ago)
        print(received_reviews, profile)
        if received_reviews.exists():
            weekly_email(profile, received_reviews)