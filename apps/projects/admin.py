from django.contrib import admin
from .models import Technology, Project, Comment, Vote

admin.site.register(Technology)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Vote)
