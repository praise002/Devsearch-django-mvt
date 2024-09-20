from django.test import TestCase
from apps.messaging.models import Message
from apps.common.utils import TestUtil

class MessageModelTest(TestCase):

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

    def test_message_str(self):
        """Test the Message model's string representation"""
        self.assertEqual(str(self.message), 'Test Subject')

