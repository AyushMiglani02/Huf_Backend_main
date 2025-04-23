"""health_umbrella_foundation_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("home.urls")),
    path("", RedirectView.as_view(url="home/", permanent=True)),
    path("disease/", include("disease.urls")),
    path("footer/", include("footer.urls")),
    path("ejournal/", include("ejournal.urls")),
    path("feedback/", include("feedback.urls")),
    path("pathy/", include("pathy.urls")),
    path("header/", include("header.urls")),
    path("clinics/", include("clinics.urls")),
    path("members/", include("members.urls")),
    path("user-forms/", include("user_forms.urls")),
    path("analytics/", include("analytics.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
