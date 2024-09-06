
from django.contrib.postgres.search import SearchVector, \
    SearchQuery, SearchRank, TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile

def paginate_profiles(request, profiles, results):
    page = request.GET.get('page') # e.g., ?page=2
    paginator = Paginator(profiles, results) # obj_list, per_page
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)
        
    left_index = max(1, profiles.number - 4) # profiles.num = curr_page
    right_index = min(paginator.num_pages + 1, profiles.number + 5)
        
    custom_range = range(left_index, right_index)
    
    return custom_range, profiles
    
def developers_search(request):
    search_query = request.GET.get('search_query', '')  # Default to an empty string if not provided

    profiles = Profile.objects.all()  
    
    if search_query:
        # search_vector = SearchVector('user__username', weight='A') + \
        #     SearchVector('short_intro', weight='B') 
        # search_query_obj = SearchQuery(search_query)
        # profiles = Profile.objects.annotate(
        #     search=search_vector,
        #     rank=SearchRank(search_vector, search_query_obj)
        # ).filter(rank__gte=0.2).distinct().order_by('-rank')
        profiles = Profile.objects.annotate(
            similarity=TrigramSimilarity('user__username', search_query),
        ).filter(similarity__gt=0.1).order_by('-similarity')
        
    return profiles, search_query

