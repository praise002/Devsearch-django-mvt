from django.urls import path
from django.views.decorators.cache import cache_page
from .import views

app_name = 'messages'

urlpatterns = [
    path('inbox/', views.Inbox.as_view(), name='inbox'),
    path('message/<str:id>/', cache_page(60 * 15)(views.ViewMessage.as_view()), name='message'),
    path('message/create_message/<str:id>/', views.CreateMessage.as_view(), name='create_message'),
]
