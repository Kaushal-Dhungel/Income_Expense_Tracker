"""Itracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

react_routes = getattr(settings, 'REACT_ROUTES', [])

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register',RegisterView.as_view(),name = "register"),
    path('checkuser',CheckUser.as_view(),name = "checkuser"),
    path('getname',GetNameView.as_view(),name = "getname"),
    path('',homeView, name = "homeview"),
    path('main/',include('mainapp.urls'), name = "main"),
    url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),
]

for route in react_routes:
    urlpatterns += [
        path(f'{route}',homeView, name = 'homeView'),
    ]