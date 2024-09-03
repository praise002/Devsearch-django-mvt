
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
        context = {
            'message_requests': message_requests,
            'unread_count': unread_count,
        }
        return render(request, 'messaging/inbox.html', context)
    
class ViewMessage(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        message = profile.messages.get(id=kwargs('id'))
        
        if message.is_read == False:
            message.is_read = True
            message.save()
        
        context = {'message': message}
        return render(request, 'messaging/message_list.html', context)

class CreateMessage(View):
    def get(self, request):
        form = MessageForm()
        context = {
            'form': form,
        }
        return render(request, 'messaging/message_form.html', context)
        
        
            
    def post(self, request):
        recipient = get_object_or_404(Profile, id=id)
        
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
                message.name = sender.full_name
                message.email = sender.email
            message.save()
            
            sweetify.toast(request, 'Your message was successfully sent!')
            return redirect('profiles:profile_detail', username=recipient.username)
        
        context = {
            'recipient': recipient,
            'form': form,
        }
        return render(request, 'messaging/message_form.html', context)