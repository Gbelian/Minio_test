"""
URL configuration for monprojet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from monapp.admin import custom_admin_site


# urls.py
from django.conf.urls import handler404
from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    return render(request, "monapp/404.html", {})

handler404 = custom_page_not_found_view



from django.conf.urls import handler500

def custom_error_view(request):
    return render(request, "monapp/500.html", {})

handler500 = custom_error_view


from django.conf.urls import handler403

def custom_permission_denied_view(request, exception):
    return render(request, "monapp/403.html", {})

handler403 = custom_permission_denied_view



urlpatterns = [
    path('admin', custom_admin_site.urls),
    path('', include('monapp.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

