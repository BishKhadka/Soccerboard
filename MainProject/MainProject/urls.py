"""
URL configuration for MainProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from App1 import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # the name "home1" will be used to redirect url in html, we should use the name in html

    path('', views.home, name='home1'),  #home page url (first one is path, second func, third func)
    path('api/teams/', views.team_list, name='team-list'),
    path('api/delete-entire-model/', views.deleteEntireModel, name='deleteEntireModel'),
    path('api/add/', views.add_data, name='add_data'),


]
