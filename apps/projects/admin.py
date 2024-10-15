from django.contrib import admin
from .models import Tag, Project, Review

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    search_fields = ('name',)
    list_filter = ('created',) 
    list_per_page = 10

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'vote_total', 'vote_ratio')
    search_fields = ('title', 'description', 'owner__user__username', 'tags__name')  
    list_filter = ('created', 'updated')  
    readonly_fields = ('slug', 'vote_total', 'vote_ratio', 'updated')  
    filter_horizontal = ('tags',)  # Display tags in a horizontal filter widget
    list_per_page = 10
    
    # Specify the order of fields
    fields = (
        'title',   
        'slug',    
        'owner', 
        'description',
        'source_link',
        'demo_link',
        'tags',
        'vote_total',
        'vote_ratio',
        'updated',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('owner').prefetch_related('tags')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'reviewer', 'value', 'created')
    search_fields = ('project__title', 'reviewer__user__username', 'value')  
    list_filter = ('value',) 
    readonly_fields = ('created',)  
    list_per_page = 10

