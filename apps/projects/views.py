from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from apps.accounts.mixins import LoginRequiredMixin
from .forms import ReviewForm, ProjectForm
from .models import Project, Tag
import sweetify

class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.all()
        context = {'projects': projects}
        return render(request, 'projects/projects_list.html', context)

class ProjectDetailView(View):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('id'))
        form = ReviewForm()
        context = {'project': project, 'form': form}
        return render(request, 'projects/project_detail.html', context)
    
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('id'))
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.reviewer = request.user.profile
        review.save()
        
        project.review_percentage # update the percentage count
        
        sweetify.toast(request, 'Your review was successfully submitted!')
        return redirect(request, pk=project.id)

class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProjectForm()
        context = {'form': form}
        return render(request, "projects/project_form.html", context)
    
    def post(self, request):
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        profile = request.user.profile
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            
            for tag in newtags:
                tag, _ = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            sweetify.toast(request, 'Project added successfully')
            return redirect('profiles:account')
        
        context = {'form': form}
        return render(request, "projects/project_form.html", context)

class ProjectEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        project = profile.projects.get(id=kwargs.get('id'))
        form = ProjectForm(instance=project)
        context = {'form': form}
        return render(request, "projects/project_form.html", context)
        
    def post(self, request, *args, **kwargs):
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        
        profile = request.user.profile
        project = profile.projects.get(id=kwargs.get('id'))
        form = ProjectForm(request.POST, request.FILES, instance=project)
        
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, _ = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            sweetify.toast(request, 'Project updated successfully')
            return redirect('profiles:account')
        
        context = {'form': form, 'project': project}
        return render(request, "projects/project_form.html", context)

class ProjectDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        project = profile.projects.get(id=kwargs.get('id'))
        
        context = {'object': project}
        return render(request, 'delete_template.html', context)
    
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        project = profile.projects.get(id=kwargs.get('id'))
        project.delete()
        return redirect('profiles:account')