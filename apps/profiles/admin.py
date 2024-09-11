from django.contrib import admin
from .models import Skill, Profile

class SkillAdmin(admin.ModelAdmin):
    list_filter = ('user',) 
    search_fields = ('name', 'user__user__username')
    readonly_fields = ('id',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_intro', 'location')
    search_fields = ('user__username', 'short_intro', 'location') 
    readonly_fields = ('id', 'updated', 'created') 
    list_filter = ('created',) 
    
admin.site.register(Skill, SkillAdmin)
admin.site.register(Profile, ProfileAdmin)

# list_display, list_filter, readonly_fields, search_fields
# exclude, list_display_links, list_per_page