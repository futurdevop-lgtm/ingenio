"""
URL configuration for talent_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('', TemplateView.as_view(template_name='index.html'), name='accueil'),
    path('app/', include(('portal.urls', 'portal'), namespace='portal')),
    path('api/comptes/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('api/profils/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('api/projets/', include(('projects.urls', 'projects'), namespace='projects')),
    path('api/recherche/', include(('search.urls', 'search'), namespace='search')),
    path('api/tableau/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('api/comm/', include(('communications.urls', 'communications'), namespace='communications')),
    path('api/securite/', include(('security.urls', 'security'), namespace='security')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
