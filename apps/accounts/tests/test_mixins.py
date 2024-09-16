from apps.common.utils import TestUtil
from django.test import TestCase, Client
from django.urls import reverse

class MixinTests(TestCase):
    login_url = reverse('accounts:login')
    logout_url = reverse('accounts:logout')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        
    def test_authenticated_user_redirect(self):
        user = self.user 
        response = self.client.post(
            self.login_url,
            {"email": user.email, "password": "testpassword"},
        )
        self.assertRedirects(
            response,
            reverse('projects:projects_list'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
    def test_unauthenticated_user_redirect(self):
        response = self.client.post(
            self.logout_url,
        )
        self.assertRedirects(
            response,
            reverse('accounts:login'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
    def test_unauthenticated_user_ajax(self):
        # Simulate an AJAX request
        response = self.client.post(self.logout_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)  
        self.assertJSONEqual(response.content, {"status": "error", "message": "You must login first!"})
        
        
    
