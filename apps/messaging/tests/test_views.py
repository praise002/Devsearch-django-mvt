from apps.messaging.forms import MessageForm
from apps.messaging.models import Message
from apps.common.utils import TestUtil
from django.test import TestCase, Client
from django.urls import reverse
import json

class InboxViewTests(TestCase):
    login_url = reverse('accounts:login')
    inbox_url = reverse('messages:inbox')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        self.other_user = TestUtil.other_user()
        self.other_profile = self.other_user.profile
        
        self.message = Message.objects.create(
            sender=self.other_profile,
            recipient=self.profile,
            subject="Test Message",
            body="Test body",
            is_read=False,
        )
    
    def test_inbox_view(self):
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Message')
        self.assertEqual(response.context['unread_count'], 1)
        self.assertTemplateUsed(response, 'messaging/inbox.html')
        
class ViewMessageTests(TestCase):
    login_url = reverse('accounts:login')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        self.other_user = TestUtil.other_user()
        self.other_profile = self.other_user.profile
        
        self.message = Message.objects.create(
            sender=self.other_profile,
            recipient=self.profile,
            subject="Test Message",
            body="Test body",
            is_read=False,
        )
        
        self.message_detail = reverse('messages:message', args=[self.message.id])
    
    def test_view_message(self):
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        response = self.client.get(self.message_detail)
        self.assertEqual(response.status_code, 200)
        # Check if message is marked as read
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)
        self.assertTemplateUsed(response, 'messaging/message_detail.html')
        
class CreateMessageTests(TestCase):
    login_url = reverse('accounts:login')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.recipient = self.user.profile
        self.other_user = TestUtil.other_user()
        self.other_profile = self.other_user.profile
        self.create_msg_url = reverse('messages:create_message', args=[self.recipient.id])

    def test_create_message(self):
        # GET
        response = self.client.get(self.create_msg_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/message_form.html')
        self.assertIsInstance(response.context['form'], MessageForm)
        
        # POST
        self.client.post(
            self.login_url,
            {"email": self.other_user.email, "password": "testpassword"},
        )
        
        data = {
            'subject': 'New Message',
            'body': 'This is a test message.'
        }
        response = self.client.post(self.create_msg_url, data)
        
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "Your message was successfully sent!")
        
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Message.objects.filter(subject='New Message').exists())
        
class DeleteMessageTests(TestCase):
    login_url = reverse('accounts:login')
    inbox_url = reverse('messages:inbox')
    
    def setUp(self):
        self.user = TestUtil.verified_user()
        self.other_user = TestUtil.other_user()
        
        self.sender = self.user.profile
        self.recipient = self.other_user.profile
        self.message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject='Test Subject',
            body='This is a test message.'
        )
        
        self.delete_url = reverse('messages:delete_message', args=[self.message.id])

    def test_delete_message(self):
        # GET
        self.client.post(
            self.login_url,
            {"email": self.other_user.email, "password": "testpassword"},
        )
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/delete_template.html')

        # POST
        response = self.client.post(self.delete_url)
        
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "Message successfully deleted!")
        
        self.assertRedirects(
            response,
            self.inbox_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())  

