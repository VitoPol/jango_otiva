"""day_47 URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads import views
from datasets.fill_scripts import *
from users import views as v

router = routers.SimpleRouter()
router.register('locations', v.LocationsViewSet)

urlpatterns = [
    path('', views.index),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('ads/', include("ads.urls")),
    path('users/', include("users.urls")),

    path('fill_users/', fill_users_db),
    path('fill_categories/', fill_categories_db),
    path('fill_locations/', fill_location_db),
    path('fill_ads/', fill_ads_db)
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
