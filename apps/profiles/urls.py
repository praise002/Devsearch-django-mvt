from django.urls import path
from .import views

app_name = "profiles"

urlpatterns = [
    # URL for viewing a specific user's profile by username
    path('<str:username>/', views.ProfileDetailView.as_view(), name="profile_view"),

    # URL for editing the current user's profile
    path('edit/', views.EditView.as_view(), name="profile_edit"),

    # URL for editing the current user's skills
    path('skills/edit/', views.SkillEditView.as_view(), name="skill_edit"),
]
