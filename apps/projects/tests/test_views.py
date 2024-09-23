from apps.projects.models import Project, Tag, Review
from apps.projects.forms import ProjectForm, ReviewForm
from apps.common.utils import TestUtil
from django.test import TestCase, Client
from django.urls import reverse
import json

class ProjectListViewTests(TestCase):
    project_list = reverse('projects:projects_list')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        self.project = Project.objects.create(
            title="Sample Project",
            owner=self.profile,
            description="A sample project description",
        )
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        
    def test_list_view(self):
        response = self.client.get(self.project_list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/projects_list.html') 
        
    def test_search_query(self):
        # test for nonexistent
        response = self.client.get(self.project_list, {'search_query': 'Nonexistent'})
        
        self.assertEqual(response.context['search_query'], 'Nonexistent')
        self.assertTemplateUsed(response, 'projects/projects_list.html')
        
        # test for existent
        response = self.client.get(self.project_list, {'search_query': 'Sample Project'})
        
        self.assertEqual(response.context['search_query'], 'Sample Project')
        self.assertTemplateUsed(response, 'projects/projects_list.html')
        
class ProjectDetailViewTest(TestCase):
    login_url = reverse('accounts:login')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        self.other_user = TestUtil.other_user()
        self.other_profile = self.other_user.profile
        
        self.tag = Tag.objects.create(name="Django")
        self.project = Project.objects.create(
            title="Sample Project",
            owner=self.profile,
            description="A sample project description",
        )
        self.project.tags.add(self.tag)
        
        self.project_detail = reverse('projects:project_detail', args=[self.project.slug])
        
    def test_project_detail(self):
        # GET
        response = self.client.get(self.project_detail)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('projects/project_detail.html')
        self.assertEqual(response.context['project'], self.project)
        self.assertIsInstance(response.context['form'], ReviewForm)
        
        # Test GET request for a non-existent project
        non_existent_url = reverse('projects:project_detail', kwargs={'slug': 'non-existent-slug'})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, 404)
        
        # POST
        # Invalid Review
        self.client.post(
            self.login_url,
            {"email": self.other_user.email, "password": "testpassword"},
        )
        form_data = {
            'value': '',  
            'content': ''  
        }
        response = self.client.post(self.project_detail, form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Review.objects.count(), 0) 
        
        # Valid Review
        form_data = {
            'value': 'up', 
            'content': 'Great project!'
        }
        response = self.client.post(self.project_detail, form_data)
        
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "Your review was successfully submitted!")
        
        # Verify review percentage update
        self.project.refresh_from_db()
        self.assertTrue(Review.objects.filter(project=self.project, reviewer=self.other_profile).exists())
        self.assertGreater(self.project.vote_total, 0)
        
class ProjectCreateViewTests(TestCase):
    add_project_url = reverse('projects:project_add')
    login_url = reverse('accounts:login')
    account_view = reverse('profiles:account')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
    def test_project(self):
        # GET
        # log in user
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        response = self.client.get(self.add_project_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        
        # POST
        # Test for invalid POST
        data = {
            'title': ''  
        }
        response = self.client.post(self.add_project_url, data)
        
        # Test that the form submission fails
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')
        self.assertFalse(response.context['form'].is_valid()) 
        
        # Check that no project is created in the database
        self.assertFalse(Project.objects.exists())
        
        # Test for valid POST
        data = {
            'title': 'E-commerce application',
            'description': 'Lorem Ipsum'
        }
        response = self.client.post(self.add_project_url, data)
        
        # Test that the form submission is successful
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "Project added successfully")
        
        self.assertRedirects(
            response,
            self.account_view,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
        # Check that the project is saved in the database
        project = Project.objects.get(title='E-commerce application')
        self.assertEqual(project.owner, self.profile)
        self.assertEqual(project.description, 'Lorem Ipsum')
        
class ProjectEditViewTests(TestCase):
    login_url = reverse('accounts:login')
    account_view = reverse('profiles:account')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
        self.tag = Tag.objects.create(name="Django")
        self.project = Project.objects.create(
            title="Sample Project",
            owner=self.profile,
            description="A sample project description",
        )
        self.project.tags.add(self.tag)
        
        self.project_edit = reverse('projects:project_edit', args=[self.project.slug])
        
    
    def test_project(self):
        # GET
        # log in user
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        
        response = self.client.get(self.project_edit)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_form.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertEqual(response.context['form'].instance, self.project)
        
        # POST
        # Invalid POST
        data = {'title': ''}  # Invalid data, title is required
        response = self.client.post(self.project_edit, data)
        
        self.assertEqual(response.status_code, 200)  # Should re-render the form
        
        self.project.refresh_from_db()  # Ensure the project was not changed
        self.assertEqual(self.project.title, 'Sample Project')
        
        # valid POST
        data = {'title': 'Updated Project', 'description': "A sample project description"}
        
        response = self.client.post(self.project_edit, data)

        self.assertEqual(response.status_code, 302)  # Redirects to account page
        self.project.refresh_from_db()  # Reload the project instance from the database
        self.assertEqual(self.project.title, 'Updated Project')
        
        session_sweetify = json.loads(self.client.session.get('sweetify'))
        self.assertEqual(session_sweetify.get('title'), "Project updated successfully")
        
class ProjectDeleteViewTests(TestCase):
    login_url = reverse('accounts:login')
    account_view = reverse('profiles:account')
    
    def setUp(self):
        self.client = Client()
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        
        self.project = Project.objects.create(
            title="Sample Project",
            owner=self.profile,
            description="A sample project description",
        )
        
        self.delete_url = reverse('projects:project_delete', args=[self.project.slug])
        
        # log in user
        self.client.post(
            self.login_url,
            {"email": self.user.email, "password": "testpassword"},
        )
        
    def test_delete(self):
        # GET
        # test project belongs to user
        response = self.client.get(self.delete_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/delete_template.html')
        self.assertEqual(response.context['object'], self.project)
        
        # test project doesn't belong to user
        other_user = TestUtil.other_user()
        other_profile = other_user.profile
        other_project = Project.objects.create(
            title="Other Project",
            owner=other_profile,
            description="A sample project description",
        )
        
        other_url = reverse('profiles:skill_delete', args=[other_project.slug])
        
        response = self.client.get(other_url)
        
        self.assertEqual(response.status_code, 404)
        
        # POST
        # delete project that belongs to user
        response = self.client.post(self.delete_url)
        
        self.assertEqual(Project.objects.filter(id=self.project.id).count(), 0)
        
        self.assertRedirects(
            response,
            self.account_view,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        
        # test project doesn't belong to user
        response = self.client.post(other_url)
        
        self.assertEqual(response.status_code, 404)
