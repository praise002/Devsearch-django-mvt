
from django.contrib.postgres.search import SearchVector, \
    SearchQuery, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile

def paginate_profiles(request, profiles, results):
    page = request.GET.get('page') # e.g., ?page=2
    paginator = Paginator(profiles, results) # obj_list, per_page
    
    try:
        profiles = paginator.page(page)
        print(profiles)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
        print(profiles)
    except EmptyPage:
        page = paginator.num_pages # return total num of pages
        profiles = paginator.page(page)
        print(profiles)
        
    left_index = (int(page) - 4)
    
    if left_index < 1:
        left_index = 1
        
    right_index = (int(page) + 5)
    
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
        
    custom_range = range(left_index, right_index)
    
    return custom_range, profiles
    
def developers_search(request):
    search_query = request.GET.get('search_query', '')  # Default to an empty string if not provided

    if search_query:
        search_vector = SearchVector('user__username', weight='A') + \
            SearchVector('short_intro', weight='B') 
        search_query_obj = SearchQuery(search_query)
        profiles = Profile.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query_obj)
        ).filter(rank__gte=0.2).distinct().order_by('-rank')
    else:
        profiles = Profile.objects.all()  

    return profiles, search_query

# TODO: MIGHT FIX LATER TO USE ICONTAINS OR TRIGRAM SIMILARITY
