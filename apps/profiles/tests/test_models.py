from apps.profiles.models import Skill
from apps.common.utils import TestUtil
from django.test import TestCase
from django.urls import reverse


class SkillModelTests(TestCase):
    def setUp(self):
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile

        # Create a skill instance
        self.skill = Skill.objects.create(
            name="Django",
            description="A framework for web development",
            user=self.profile
        )
        
    def test_skill_str(self):
        self.assertEqual(str(self.skill), "Django")
        
class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
    def test_str_method(self):
        self.assertEqual(str(self.profile), 'Test Verified')
        
    def test_get_absolute_url(self):
        expected_url = reverse('profiles:profile_detail', kwargs={'username': self.user.username})
        self.assertEqual(self.profile.get_absolute_url(), expected_url)
        
    def test_image_url(self):
        profile = self.profile
        
        # Test with no photo
        profile.photo = None
        self.assertEqual(profile.image_url, '')
        
        # Test the image_url property with a valid image
        profile.photo = '/media/photos/2024/09/01/test_image.jpg'
        profile.save()
        self.assertEqual(profile.image_url, profile.photo.url)
        
    # def tearDown(self):
    #     self.profile.photo.delete(save=False)