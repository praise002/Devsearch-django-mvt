from django.urls import path
from .import views

app_name = "profiles"

urlpatterns = [
    path('edit/', views.EditView.as_view(), name="edit"),
]
