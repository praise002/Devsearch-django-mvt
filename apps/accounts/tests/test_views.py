from apps.accounts.forms import RegistrationForm, LoginForm
from apps.accounts.models import User
from apps.accounts.senders import email_verification_generate_token
from apps.common.utils import TestUtil
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from unittest.mock import patch
import json
import uuid

valid_data = {
    'first_name': 'Test',
    'last_name': 'User',
    'username': 'test-user',
    'email': 'testuser@example.com',
    'password1': 'strong_password',
    'password2': 'strong_password',
}

invalid_data = {
    'first_name': 'Test',
    'last_name': 'User',
    'username': 'test-user',
    'email': 'invalid_email',
    'password1': 'short',
    'password2': 'short',
}

class TestAccounts(TestCase):
    register_url = reverse('accounts:register')
    login_url = reverse('accounts:login')
    logout_url = reverse('accounts:logout')
    logout_all_url = reverse('accounts:logout_all_devices')
    # verify_email_url = reverse('accounts:verify_email')
    resend_verification_email_url = reverse('accounts:resend_verification_email')
    
    def setUp(self):
        """Set up the test client and initial data."""
        self.client = Client()
        self.new_user = TestUtil.new_user()
        self.verified_user = TestUtil.verified_user()
        self.valid_data = valid_data
        self.invalid_data = invalid_data
    
    @patch('apps.accounts.senders.SendEmail.verification')
    def test_register(self, mock_verification):
        # GET
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)
        
        # POST
        # Verify that a new user can be registered successfully
        response = self.client.post(self.register_url, self.valid_data)
        
        self.assertTemplateUsed(response, 'accounts/email_verification_sent.html')
        user = User.objects.get(email=self.valid_data['email'])
        self.assertEqual(self.client.session['verification_email'], user.email)
        mock_verification.assert_called_once_with(response.wsgi_request, user)

        # Verify that a user with the same email cannot be registered again
        response = self.client.post(self.register_url, self.valid_data)
        self.assertIsNotNone(response.context.get("form").errors)
        
        # Verify that a invalid registration data renders the signup template again
        response = self.client.post(self.register_url, self.invalid_data)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)
    
    @patch('apps.accounts.senders.SendEmail.welcome')
    def test_verify_email(self, mock_welcome):
        # Verify that the email verification succeeds with a valid link
        new_user = self.new_user
        uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
        token = email_verification_generate_token.make_token(new_user)
        response = self.client.get(
            reverse('accounts:verify_email', 
                    kwargs={'uidb64': uidb64, 'token': token, 'user_id': new_user.pk})
        )

        self.assertRedirects(
            response,
            self.login_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_email_verified)
        mock_welcome.assert_called_once_with(response.wsgi_request, new_user)
        
        # Verify that the email verification fails with an invalid link
        fake_uidb64 = urlsafe_base64_encode(force_bytes(uuid.uuid4()))

        response = self.client.get(
            reverse('accounts:verify_email', kwargs={'uidb64': fake_uidb64, 'token': token, 'user_id': new_user.pk})
        )
        
        self.assertTemplateUsed('accounts/email_verification_failed.html')
        self.assertContains(response, 'Email Verification Failed')

        # Verify that it redirects if user does not exist
        with self.assertRaises(User.DoesNotExist): 
            User.objects.get(id='1aed656f-0ecc-482d-9582-5fa242965f93')
        
        uidb64_fake = 'fake-uidb64'
        token_fake = 'fake-token'
        response = self.client.get(
            reverse('accounts:verify_email', kwargs={'uidb64': uidb64_fake, 'token': token_fake, 'user_id':'1aed656f-0ecc-482d-9582-5fa242965f93'})
        )
        
        self.assertRedirects(
            response,
            self.login_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
        
        # Verify verification fails if the id is different
        wrong_user_id = '1aed656f-0ecc-482d-9582-5fa242965f93'  
        uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
        token = email_verification_generate_token.make_token(new_user)
        response = self.client.get(
            reverse('accounts:verify_email', 
                    kwargs={'uidb64': uidb64, 'token': token, 'user_id': wrong_user_id})
        )
        
        # Check for sweetify error in session
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "You entered an invalid link")
        
        self.assertRedirects(
            response,
            reverse('accounts:login'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
            
    @patch('apps.accounts.senders.SendEmail.verification')
    def test_resend_verification_email(self, mock_verification):
        new_user = self.new_user
        
        # Verify that an unverified user can get a new email
        session = self.client.session  # Get the session
        session["verification_email"] = new_user.email  # Set the session variable
        session.save()  # Explicitly save the session
        
        # Then, attempt to resend the activation email
        response = self.client.get(
            self.resend_verification_email_url,
        )
        self.assertTemplateUsed(response, "accounts/email_verification_sent.html")
        
        # Verify the mock function was called with the correct arguments
        mock_verification.assert_called_once_with(response.wsgi_request, new_user)
        
        
        # Verify that a verified user cannot get a new email
        new_user.is_email_verified = True
        new_user.save()
        
        response = self.client.get(
            self.resend_verification_email_url,
        )
        
        self.assertRedirects(
            response,
            self.login_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
        
        # Verify that an error is raised when attempting to resend the activation email for a user that doesn't exist
        with self.assertRaises(User.DoesNotExist): 
            User.objects.get(email='invalid_email@example.com')
            
        response = self.client.get(
            self.resend_verification_email_url,
        )
        
        self.assertRedirects(
            response,
            self.login_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
    def test_login(self):
        # GET #
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertIsInstance(response.context['form'], LoginForm)
        
        # POST 
        new_user = self.new_user

        # Test for invalid credentials
        response = self.client.post(
            reverse('accounts:login'),
            {"email": "invalid@email.com", "password": "invalidpassword"},
        )
        
        # Check for sweetify error in session
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify['title'], "Invalid Credentials")
        
        self.assertRedirects(
            response,
            reverse('accounts:login'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
         # Test for unverified credentials (email)
        response = self.client.post(
            reverse('accounts:login'),
            {"email": new_user.email, "password": "testpassword"},
        )
        self.assertTemplateUsed(response, "accounts/email_verification_sent.html")
        
         # Test for valid credentials and verified email address
        new_user.is_email_verified = True
        new_user.save()
        response = self.client.post(
            reverse('accounts:login'),
            {"email": new_user.email, "password": "testpassword"},
        )
        self.assertRedirects(
            response,
            reverse('projects:projects_list'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_logout(self):
        verified_user = self.verified_user

        # Ensures A user logs out successfully
        self.client.login(email=verified_user.email, password="testpassword")
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(
            response,
            reverse('accounts:login'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
    def test_logout_all_devices(self):
        verified_user = self.verified_user

        self.client.login(email=verified_user.email, password="testpassword")
        response = self.client.post(reverse('accounts:logout_all_devices'))
        self.assertRedirects(
            response,
            reverse('accounts:login'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        session = self.client.session
        self.assertFalse(session.keys(), "Session was not flushed as expected.")

