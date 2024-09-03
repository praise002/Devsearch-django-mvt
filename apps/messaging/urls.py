from django.urls import path
from .import views

app_name = 'messages'

urlpatterns = [
    path('inbox/', views.Inbox.as_view(), name='inbox'),
    path('message/<str:id>/', views.ViewMessage.as_view(), name='message'),
    path('message/create_message/<str:id>/', views.ViewMessage.as_view(), name='create_message'),
]
