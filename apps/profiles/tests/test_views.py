from apps.projects.models import Project
from apps.profiles.models import Skill, Profile
from apps.common.utils import TestUtil
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.forms import UserEditForm
from apps.profiles.forms import ProfileEditForm, SkillForm
import json

class TestAccountView(TestCase):
    login_url = reverse('accounts:login')
    account_view = reverse('profiles:account')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
        self.skill1 = Skill.objects.create(name='Python', user=self.user.profile)
        self.skill2 = Skill.objects.create(name='Django', user=self.user.profile)
        
    def test_account_view(self):
        user = self.user
        # test for get request while logged out
        response = self.client.get(self.account_view)
        self.assertRedirects(
            response,
            f'{self.login_url}?next=/en/profiles/account/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
        # test for get request while logged in 
        self.client.post(
            self.login_url,
            {"email": user.email, "password": "testpassword"},
        )
        response = self.client.get(self.account_view)
        
        self.assertTemplateUsed(response, 'profiles/account.html')
        self.assertEqual(response.context['profile'], self.profile)
        
        skills_in_context = response.context['skills']
        self.assertIn(self.skill1, skills_in_context)
        self.assertIn(self.skill2, skills_in_context)

class ProfileListViewTests(TestCase):
    profile_list = reverse('profiles:profile_list')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile1 = self.user.profile
        self.other_user = TestUtil.other_user()
        self.profile2 = self.other_user.profile
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        
    def test_list_view(self):
        response = self.client.get(self.profile_list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/index.html') 
        
    def test_search_query(self):
        # test for nonexistent
        response = self.client.get(self.profile_list, {'search_query': 'Nonexistent'})
        
        self.assertEqual(response.context['search_query'], 'Nonexistent')
        self.assertTemplateUsed(response, 'common/index.html')
        
        # test for existent
        response = self.client.get(self.profile_list, {'search_query': 'test'})
        print(response.content)
        
        self.assertEqual(response.context['search_query'], 'test')
        self.assertTemplateUsed(response, 'common/index.html')
    
class ProfileDetailViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
        self.skill_with_desc = Skill.objects.create(user=self.user.profile, name="Python", description="Programming Language")
        self.skill_without_desc = Skill.objects.create(user=self.user.profile, name="Django", description="")
        
        self.project = Project.objects.create(owner=self.profile, title="Test Project")
        
        self.profile_detail = reverse('profiles:profile_detail', kwargs={'username': self.user.username})
        
    def test_profile_detail(self):
        response = self.client.get(self.profile_detail)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('profiles/profile.html')
        self.assertEqual(response.context['profile'], self.profile)
        
        top_skills = response.context['top_skills']
        self.assertIn(self.skill_with_desc, top_skills)
        self.assertNotIn(self.skill_without_desc, top_skills)
        
        other_skills = response.context['other_skills']
        self.assertIn(self.skill_without_desc, other_skills)
        self.assertNotIn(self.skill_with_desc, other_skills)


class ProfileEditViewTests(TestCase):
    edit_url = reverse('profiles:profile_edit')
    profiles_url = reverse('profiles:account')
    login_url = reverse('accounts:login')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
    def test_get_profile_edit_view(self):
        # GET
        # log in user
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        response = self.client.get(self.edit_url)
        
        self.assertTemplateUsed(response, 'profiles/edit.html')
        self.assertIsInstance(response.context['user_form'], UserEditForm)
        self.assertIsInstance(response.context['profile_form'], ProfileEditForm)
        
        # POST
        data = {
            "first_name": "Tems",
            "last_name": "Verified",
            "email": "testverifieduser@example.com",
            "is_email_verified": True,
            "password": "testpassword",
            "bio": "Updated bio"
        }
        response = self.client.post(self.edit_url, data)
        
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        
        self.assertEqual(self.user.first_name, 'Tems')
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertRedirects(
            response,
            self.profiles_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

class SkillCreateViewTests(TestCase):
    add_skill_url = reverse('profiles:skill_add')
    login_url = reverse('accounts:login')
    profiles_url = reverse('profiles:account')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
    def test_skill(self):
        # GET
        # log in user
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        response = self.client.get(self.add_skill_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/skill_form.html')
        self.assertIsInstance(response.context['form'], SkillForm)
        
        # POST
        # Test for invalid POST
        data = {
            'name': ''  # Invalid because name is required
        }
        response = self.client.post(self.add_skill_url, data)
        
        # Test that the form submission fails
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/skill_form.html')
        self.assertFalse(response.context['form'].is_valid())
        
        # Check that no skill is created in the database
        self.assertFalse(Skill.objects.exists())
        
        # Test for valid POST
        data = {
            'name': 'Python',
            'description': 'Experienced in Python programming'
        }
        response = self.client.post(self.add_skill_url, data)
        
        # Test that the form submission is successful
        self.assertRedirects(
            response,
            self.profiles_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
        # Check that the skill is saved in the database
        skill = Skill.objects.get(name='Python')
        self.assertEqual(skill.user, self.user.profile)
        self.assertEqual(skill.description, 'Experienced in Python programming')

class SkillEditViewTests(TestCase):
    login_url = reverse('accounts:login')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        self.skill = Skill.objects.create(name='Initial Skill', user=self.profile)
        
        self.edit_url = reverse('profiles:skill_edit', kwargs={'id': self.skill.id})
    
    def test_skill(self):
        # GET
        # log in user
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/skill_form.html')
        self.assertIsInstance(response.context['form'], SkillForm)
        self.assertEqual(response.context['form'].instance, self.skill)
        
        # POST
        # Invalid POST
        data = {'name': ''}  # Invalid data, name is required
        response = self.client.post(self.edit_url, data)
        
        self.assertEqual(response.status_code, 200)  # Should re-render the form
        
        self.skill.refresh_from_db()  # Ensure the skill was not changed
        self.assertEqual(self.skill.name, 'Initial Skill')
        
        # valid POST
        data = {'name': 'Updated Skill'}
        
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, 302)  # Redirects to account page
        self.skill.refresh_from_db()  # Reload the skill instance from the database
        self.assertEqual(self.skill.name, 'Updated Skill')
        
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "Skill was updated successfully!")

class SkillDeleteViewTests(TestCase):
    login_url = reverse('accounts:login')
    profiles_url = reverse('profiles:account')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        self.skill = Skill.objects.create(name='Test Skill', user=self.profile)
        
        self.delete_url = reverse('profiles:skill_delete', args=[self.skill.id])
        
        # log in user
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        
    def test_delete(self):
        # GET
        # test skill belongs to user
        response = self.client.get(self.delete_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/delete_template.html')
        self.assertEqual(response.context['object'], self.skill)
        
        # test skill doesn't belong to user
        other_user = TestUtil.other_user()
        other_profile = other_user.profile
        other_skill = Skill.objects.create(name='Other Skill', user=other_profile)
        
        other_url = reverse('profiles:skill_delete', args=[other_skill.id])
        
        response = self.client.get(other_url)
        
        self.assertEqual(response.status_code, 404)
        
        # POST
        # delete skill that belongs to user
        response = self.client.post(self.delete_url)
        
        self.assertEqual(Skill.objects.filter(id=self.skill.id).count(), 0)
        
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "Skill was deleted successfully")
        
        self.assertRedirects(
            response,
            self.profiles_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
        # test skill doesn't belong to user
        response = self.client.post(other_url)
        
        self.assertEqual(response.status_code, 404)
        
        
# coverage run --source='.' manage.py test myapp
# python manage.py test apps.profiles.tests.test_model   
# coverage run --source=apps/profiles manage.py test apps/profiles
# disable caching for it to work