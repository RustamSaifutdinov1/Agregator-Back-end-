"""AllCliniсs URL Configuration

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
from django.conf.urls.static import static

from Catalog.views import *
from AllCliniсs import settings
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'clinics', ClinicsViewSet, basename='Clinics')

routerCategory = routers.SimpleRouter()
routerCategory.register(r'category', ClinicCategoryViewSet, basename='Category')


routerDoctor = routers.SimpleRouter()
routerDoctor.register(r'doctors', DoctorsViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(routerCategory.urls)),
    path('api/v1/', include(routerDoctor.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

