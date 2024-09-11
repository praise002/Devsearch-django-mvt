from django.test import TestCase
from apps.accounts.models import User

class UserModelTests(TestCase):
    def setUp(self):
        """Create a User instance for use in tests."""
        self.user = User.objects.create_user(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="testpassword123"
        )
        
    def test_full_name(self):
        """Test the full_name property."""
        self.assertEqual(self.user.full_name, "Test User")
        
    def test_user_str(self):
        """Test the User model's __str__ method returns the correct full name."""
        self.assertEqual(str(self.user), self.user.full_name)
        
# coverage run --source=apps/accounts manage.py test apps/accounts/


        
    
        
    
        
        
        
# py manage.py test
# py manage.py test --verbosity 2
# py manage.py test catalog.tests.test_models.YourTestClass.test_one_plus_one_equals_two
