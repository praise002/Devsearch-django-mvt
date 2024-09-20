from django.contrib.postgres.search import SearchVector, \
    SearchQuery, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from django.db import IntegrityError
from apps.projects.models import Tag

from .models import Project

def paginate_projects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
        
    # left_index = (int(page) - 4)
    
    # if left_index < 1:
    #     left_index = 1
        
    # right_index = (int(page) + 5)
    
    # if right_index > paginator.num_pages:
    #     right_index = paginator.num_pages + 1
    
    left_index = max(1, projects.number - 4) # projects.num = curr_page
    right_index = min(paginator.num_pages + 1, projects.number + 5)
        
    custom_range = range(left_index, right_index)
    
    return custom_range, projects
    
def projects_search(request):
    search_query = request.GET.get('search_query', '')  # Default to an empty string if not provided

    projects = Project.objects.all()
    
    if search_query:
        search_vector = SearchVector('title', weight='A') + \
            SearchVector('description', weight='B') 
        search_query_obj = SearchQuery(search_query)
        
        # Optimize the search query and filters
        projects = projects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query_obj)
        ).filter(
            Q(rank__gte=0.3) |
            Q(tags__name__icontains=search_query) |
            Q(owner__user__username__icontains=search_query)
            ).distinct().order_by('-rank') 
        

    return projects, search_query


def process_tags(tags_string):
    """
    Process the 'newtags' string to clean and split it into a list of tags.
    """
    tags = tags_string.replace(',', " ").split()
    return tags

def add_tags_to_project(project, tags):
    """
    Add tags to the project, creating new tags if necessary.
    """
    for tag_name in tags:
        normalized_tag = tag_name.lower()
       
        tag, _ = Tag.objects.get_or_create(name=normalized_tag)
        project.tags.add(tag)
        
