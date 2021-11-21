"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

ADMIN_URL = settings.ADMIN_URL

urlpatterns = [
    path(f"{ADMIN_URL}/", admin.site.urls),
    # Your app modules
    path("user/", include("app.user.urls", namespace="user")),
    path("forum/", include("app.forum.urls", namespace="forum")),
    path("weather/", include("app.weather.urls", namespace="weather")),
    path("alert/", include("app.alert.urls", namespace="alert")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
