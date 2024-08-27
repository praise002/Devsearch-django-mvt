from django.urls import path
from .import views

app_name = "profiles"

urlpatterns = [
    # URL for editing the current user's profile
    path('edit/', views.ProfileEditView.as_view(), name="profile_edit"),
    
    path('account/', views.AccountView.as_view(), name='account'),
    
    # URL for viewing a specific user's profile by username
    path('<str:username>/', views.ProfileDetailView.as_view(), name="profile_view"),

    # URL for adding and editing the current user's skills
    path('skill/add/', views.SkillCreateView.as_view(), name="skill_add"),
    path('skill/edit/<int:id>/', views.SkillEditView.as_view(), name="skill_edit"),
    path('skill/delete/<int:id>/', views.SkillDeleteView.as_view(), name="skill_delete"),
]
