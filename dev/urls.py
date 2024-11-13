"""
URL configuration for dev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from apps.projects.views import RedirectProjectHomeView

handler500 = 'apps.common.views.custom_server_error_view'
handler404 = 'apps.common.views.custom_404'

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', RedirectProjectHomeView.as_view()),
    path(_('accounts/'), include('apps.accounts.urls', namespace='accounts')),
    path(_('profiles/'), include('apps.profiles.urls', namespace='profiles')),
    path(_('projects/'), include('apps.projects.urls', namespace='projects')),
    path('rosetta/', include('rosetta.urls')),
    path('', include('apps.messaging.urls', namespace='messages')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, 
                          document_root=settings.STATIC_ROOT) 

