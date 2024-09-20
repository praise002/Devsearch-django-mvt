from apps.projects.models import Project, Tag, Review
from apps.common.utils import TestUtil
from django.test import TestCase
from django.urls import reverse

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = TestUtil.verified_user()
        self.profile = self.user.profile
        self.tag = Tag.objects.create(name="Django")
        self.project = Project.objects.create(
            title="Sample Project",
            owner=self.profile,
            description="A sample project description",
        )
        self.project.tags.add(self.tag)
        self.review = Review.objects.create(project=self.project, reviewer=self.profile, value='up', content="Great project!")
        
    def test_str_method(self):
        self.assertEqual(str(self.project), "Sample Project")
        
    def test_review_str(self):
        self.assertEqual(str(self.review), "up")
        
    def test_absolute_url_method(self):
        expected_url = reverse('projects:project_detail', kwargs={'id': self.project.id})
        self.assertEqual(self.project.get_absolute_url(), expected_url)
        
    def test_featured_image_url_method(self):
        project = self.project
        # Test with no featured image
        self.assertEqual(project.featured_image_url, '')
        
        # Test with featured image
        project.featured_image = '/media/featured_image/2024/09/01/test_image.jpg'
        project.save()
        self.assertEqual(project.featured_image_url, project.featured_image.url)
        
    def test_review_percentage_property(self):
        self.project.review_percentage  # This should trigger the calculation and save
        self.project.refresh_from_db()  # Reload the project after save

        # Test if vote_total and vote_ratio were calculated correctly
        self.assertEqual(self.project.vote_total, 1)  # Since we have one review
        self.assertEqual(self.project.vote_ratio, 100)
       
class TagModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name="Django")

    def test_str_method(self):
        self.assertEqual(str(self.tag), "Django")