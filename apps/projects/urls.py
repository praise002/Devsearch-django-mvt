from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'projects'

urlpatterns = [
    path('', cache_page(60 * 15)(views.ProjectListView.as_view()), name='projects_list'),
    path('add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('remove_tag/', views.RemoveTagView.as_view(), name='remove_tag'),
    path('<str:id>/', cache_page(60 * 15)(views.ProjectDetailView.as_view()), name='project_detail'),
    path('<str:id>/edit/', views.ProjectEditView.as_view(), name='project_edit'),
    path('<str:id>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
