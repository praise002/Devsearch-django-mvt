from django.db import models
from apps.profiles.models import Profile

class Technology(models.Model):
    name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'technologies'
    
class Project(models.Model):
    title = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to='featured_image/', blank=True)
    description = models.TextField()
    owner = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    feedback_percentage = models.IntegerField(default=0) # TODO: MIGHT CHANGE TO FN LATER
    source_code = models.URLField(max_length=200, blank=True)
    technology = models.ManyToManyField(Technology)
    
    def __str__(self):
        return self.title
    
    def get_vote_count():
        pass
    
    class Meta:
        ordering = ['title']
    
class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.commenter.user.full_name} on {self.project.title}"
    
class Vote(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    project = models.ForeignKey(Project, related_name='votes', on_delete=models.CASCADE)
    voter = models.ForeignKey(Profile, related_name='votes', on_delete=models.CASCADE)
    value = models.CharField(max_length=4, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'voter')  # Ensures a user can only vote once per project

    def __str__(self):
        return f"Vote by {self.voter.user.full_name} on {self.project.title}"