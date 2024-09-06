
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from apps.accounts.mixins import LoginRequiredMixin
from .forms import MessageForm
from apps.profiles.models import Profile
import sweetify

class Inbox(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        message_requests = profile.messages.all()
        unread_count = message_requests.filter(is_read=False).count()
        print(unread_count)
        context = {
            'message_requests': message_requests,
            'unread_count': unread_count,
        }
        return render(request, 'messaging/inbox.html', context)
    
class ViewMessage(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        # Use select_related to fetch related profile messages in one query
        message = get_object_or_404(profile.messages.select_related('sender__user', 'recipient'), 
                                    id=kwargs.get('id'))
        
        if message.is_read == False:
            message.is_read = True
            message.save()
        
        context = {'message': message}
        return render(request, 'messaging/message_detail.html', context)

class CreateMessage(View):
    def get(self, request, *args, **kwargs):
        form = MessageForm()
        context = {
            'form': form,
        }
        return render(request, 'messaging/message_form.html', context)
        
    def post(self, request, *args, **kwargs):
        recipient = get_object_or_404(Profile, id=kwargs.get('id'))
        
        try:
            sender = request.user.profile
        except:
            sender = None
            
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.user.full_name
                message.email = sender.user.email
            message.save()
            
            sweetify.toast(request, 'Your message was successfully sent!')
            return redirect(recipient.get_absolute_url())
        
        context = {
            'recipient': recipient,
            'form': form,
        }
        return render(request, 'messaging/message_form.html', context)