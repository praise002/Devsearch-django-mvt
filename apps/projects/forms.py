from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Project, Review

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
                  "title", "featured_image", "description",
                  "source_link", "demo_link"
                  ] 
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'content']

        labels = {
            'value': 'Place your vote',
            'content': 'Add a comment with your vote'
        }
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
        self.fields['content'].widget.attrs.update({'placeholder': 'Write your comment here...'})
        
class SearchForm(forms.Form):
    query = forms.CharField()