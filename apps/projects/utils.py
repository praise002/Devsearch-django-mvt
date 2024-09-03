from django.contrib.postgres.search import SearchVector, \
    SearchQuery, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import Project

def paginate_projects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
        print(projects)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
        print(projects)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
        print(projects)
        
    left_index = (int(page) - 4)
    
    if left_index < 1:
        left_index = 1
        
    right_index = (int(page) + 5)
    
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
        
    custom_range = range(left_index, right_index)
    
    return custom_range, projects
    
def projects_search(request):
    search_query = request.GET.get('search_query', '')  # Default to an empty string if not provided

    if search_query:
        search_vector = SearchVector('title', weight='A') + \
            SearchVector('description', weight='B') 
        search_query_obj = SearchQuery(search_query)
        projects = Project.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query_obj)
        ).filter(
            Q(rank__gte=0.3) |
            Q(tags__name__icontains=search_query) |
            Q(owner__user__username__icontains=search_query)
            ).distinct().order_by('-rank') 
    else:
        projects = Project.objects.all()  

    return projects, search_query