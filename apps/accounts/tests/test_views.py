from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.forms import RegistrationForm
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from apps.accounts.senders import email_verification_generate_token

User = get_user_model()

class TestUtil:
    def new_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Name",
            "username": "test-name",
            "email": "test@example.com",
            "password": "testpassword",
        }
        user = User.objects.create_user(**user_dict)
        return user
    
class RegisterViewTests(TestCase):
    
    def setUp(self):
        """Set up the test client and initial data."""
        self.client = Client()
        self.url = reverse('accounts:register')
        self.new_user = TestUtil.new_user()
        self.valid_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'test-user',
            'email': 'testuser@example.com',
            'password1': 'strong_password',
            'password2': 'strong_password',
        }
        self.invalid_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'test-user',
            'email': 'invalid_email',
            'password1': 'short',
            'password2': 'short',
        }
    
    def test_get_register_view(self):
        """Test GET request to the registration view returns the signup page with a form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    @patch('apps.accounts.senders.SendEmail.verification')
    def test_post_register(self, mock_verification):
        # Verify that a new user can be registered successfully
        response = self.client.post(self.url, self.valid_data)
        
        # Assert that it renders the success template
        self.assertTemplateUsed(response, 'accounts/email_verification_sent.html')
        
        # Assert user creation and email storage in session
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(email=self.valid_data['email'])
        self.assertEqual(self.client.session['verification_email'], user.email)

        # Assert SendEmail.verification was called with correct arguments
        mock_verification.assert_called_once_with(response.wsgi_request, user)
    
        # Verify that a invalid registration data renders the signup template again
        response = self.client.post(self.url, self.invalid_data)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)
        
         # Verify that a user with the same email cannot be registered again
        response = self.client.post(self.url, self.valid_data)
        self.assertIsNotNone(response.context.get("form").errors)
    
    def test_verify_email(self):
        new_user = self.new_user
        uid = urlsafe_base64_encode(force_bytes(new_user.id))
        token = email_verification_generate_token.make_token(new_user)
    
    def test_resend_verification_email(self):
        pass
    
    def test_login(self):
        pass
    
    def test_logout(self):
        pass
