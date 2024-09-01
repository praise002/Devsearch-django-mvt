from django.contrib.postgres.search import SearchVector, \
    SearchQuery, SearchRank
from .models import Profile
        
def developers_search(request):
    search_query = request.GET.get('search_query', '')  # Default to an empty string if not provided

    if search_query:
        search_vector = SearchVector('user__first_name', weight='A') + \
            SearchVector('user__last_name', weight='B') + \
            SearchVector('short_intro', weight='B') 
        search_query_obj = SearchQuery(search_query)
        profiles = Profile.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query_obj)
        ).filter(rank__gte=0.2).order_by('-rank')
    else:
        profiles = Profile.objects.all()  

    return profiles, search_query