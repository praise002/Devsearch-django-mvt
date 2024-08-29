from django.db import models
from apps.common.models import BaseModel
from apps.profiles.models import Profile
import uuid

class Tag(BaseModel):
    name = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    
class Project(BaseModel):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='featured_image/', blank=True)
    description = models.TextField()
    source_link = models.CharField(max_length=200, blank=True)
    demo_link = models.CharField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['title']
        
    @property
    def featured_image_url(self):
        try:
            url = self.featured_image
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.title
    
    @property
    def reviewers(self):
        queryset = self.review.all().values_list('owner__id', flat=True)
        return queryset
    
    @property
    def review_percentage(self):
        """
        Calculate the positive feedback percentage based on votes.
        """
        reviews = self.review.all()
        total_votes = reviews.count()
        
        if total_votes > 0:
            up_votes = reviews.filter(value='up').count()
            ratio = (up_votes / total_votes) * 100
            self.vote_total = total_votes
            self.vote_ratio = ratio
        
            self.save()
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="review")
    reviewer = models.ForeignKey(Profile, related_name='votes', on_delete=models.CASCADE)
    value = models.CharField(max_length=4, choices=VOTE_TYPE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = ('project', 'reviewer') # Ensures a user can only vote once per project
    
    def __str__(self):
        return self.value
    

#python manage.py migrate projects zero 