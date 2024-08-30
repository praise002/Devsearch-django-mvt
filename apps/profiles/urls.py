from django.urls import path
from .import views

app_name = "profiles"

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='profile_list'),
    
    # URL for editing the current user's profile
    path('edit/', views.ProfileEditView.as_view(), name="profile_edit"),
    
    path('account/', views.AccountView.as_view(), name='account'),
    
    # URL for viewing a specific user's profile by username
    path('<str:username>/', views.ProfileDetailView.as_view(), name="profile_detail"),

    # URL for adding and editing the current user's skills
    path('skill/add/', views.SkillCreateView.as_view(), name="skill_add"),
    path('skill/edit/<str:id>/', views.SkillEditView.as_view(), name="skill_edit"),
    path('skill/delete/<str:id>/', views.SkillDeleteView.as_view(), name="skill_delete"),
]
