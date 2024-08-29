from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='projects_list'),
    path('add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('<str:id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<str:id>/edit/', views.ProjectEditView.as_view(), name='project_edit'),
    path('<str:id>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
