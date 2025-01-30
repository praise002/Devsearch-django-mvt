from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'projects'

urlpatterns = [
    # path('', cache_page(60 * 15)(views.ProjectListView.as_view()), name='projects_list'),
    path('', views.ProjectListView.as_view(), name='projects_list'),
    path('add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('remove-tag/', views.RemoveTagView.as_view(), name='remove_tag'),
    # path('<slug:slug>/', cache_page(60 * 15)(views.ProjectDetailView.as_view()), name='project_detail'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<slug:slug>/edit/', views.ProjectEditView.as_view(), name='project_edit'),
    path('<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
