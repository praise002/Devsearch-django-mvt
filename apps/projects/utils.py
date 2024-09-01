from django.contrib.postgres.search import SearchVector, \
    SearchQuery, SearchRank
from django.db.models import Q

from .models import Project
        
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
            ).order_by('-rank')
    else:
        projects = Project.objects.all()  

    return projects, search_query