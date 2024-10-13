
import json
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.accounts.mixins import LoginRequiredMixin

from .forms import ReviewForm, ProjectForm
from .models import Project, Tag
from .utils import projects_search, paginate_projects, process_tags, add_tags_to_project
import sweetify
    
class ProjectListView(View):
    def get(self, request):
        projects, search_query = projects_search(request)
        
        # Prefetch related data to minimize database queries
        projects = projects.select_related('owner__user').prefetch_related('tags', 'reviews')
        
        custom_range, projects = paginate_projects(request, projects, 6)
        
        context = {
            'projects': projects,
            'search_query': search_query,
            'custom_range': custom_range,
            }
        return render(request, 'projects/projects_list.html', context)

class ProjectDetailView(View):
    def get(self, request, *args, **kwargs):
        project_slug = kwargs.get('slug') 
        
        project = get_object_or_404(
            Project.objects
            .select_related('owner__user')  # Optimize fetching owner and owner.user
            .prefetch_related('tags', 'reviews'),  # Optimize fetching tags and reviews 
            slug=project_slug
        )
        
        # Get related projects based on shared tags
        related_projects = Project.objects \
            .select_related('owner__user').filter(
                tags__in=project.tags.all()
            ).exclude(id=project.id).distinct()[:4]
        print(related_projects)
        
        form = ReviewForm()
        context = {'project': project, 
                   'form': form,
                   'related_projects': related_projects}
        return render(request, 'projects/project_detail.html', context)
    
    def post(self, request, *args, **kwargs): 
        project_slug = kwargs.get('slug') 

        project = get_object_or_404(Project, slug=project_slug)
        
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.reviewer = request.user.profile
            review.save()
        
            project.review_percentage # update the percentage count
        
            sweetify.toast(request, 'Your review was successfully submitted!')
        return redirect('projects:project_detail', slug=project.slug)

class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProjectForm()
        context = {'form': form}
        return render(request, "projects/project_form.html", context)
    
    def post(self, request):
        newtags = request.POST.get('newtags', "")  
        tags = process_tags(newtags)
        
        profile = request.user.profile
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            
            add_tags_to_project(project, tags)
            
            sweetify.toast(request, 'Project added successfully')
            return redirect('profiles:account')
        
        context = {'form': form}
        return render(request, "projects/project_form.html", context)

class ProjectEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        project_slug = kwargs.get('slug') 
        
        
        project = get_object_or_404(profile.projects, slug=project_slug)
        form = ProjectForm(instance=project)
        context = {'form': form, 'project': project}
        return render(request, "projects/project_form.html", context)
        
    def post(self, request, *args, **kwargs):
        newtags = request.POST.get('newtags', "")  
        tags = process_tags(newtags)
        
        profile = request.user.profile
        
        project_slug = kwargs.get('slug')
        
        project = get_object_or_404(profile.projects, slug=project_slug)
        
        form = ProjectForm(request.POST, request.FILES, instance=project)
        
        if form.is_valid():
            project = form.save()
            add_tags_to_project(project, tags)
            
            sweetify.toast(request, 'Project updated successfully')
            return redirect('profiles:account')
        
        context = {'form': form, 'project': project, 'newtags': " ".join(newtags)}
        return render(request, "projects/project_form.html", context)

class ProjectDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        
        project_slug = kwargs.get('slug')
        
        project = get_object_or_404(profile.projects, slug=project_slug)
        
        context = {'object': project}
        return render(request, 'common/delete_template.html', context)
    
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        project_slug = kwargs.get('slug')
        project = profile.projects.get(slug=project_slug)
        project.delete()
        return redirect('profiles:account')

@method_decorator(csrf_exempt, name='dispatch')
class RemoveTagView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        tag_id = data.get('tag_id')
        project_slug = data.get('project_slug')

        try:
            project = Project.objects.get(slug=project_slug)
            tag = Tag.objects.get(id=tag_id)
            project.tags.remove(tag)
            return JsonResponse({'success': True})
        except (Project.DoesNotExist, Tag.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Project or Tag not found'}, status=404)

# TODO: UNDERSTAND IT
# python -m pip install -U djlint - use after done with project