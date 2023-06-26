from django.urls import path, include
from soccerboard import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stats/<str:team_name>/', views.stats, name='stats'),
    path('league_table/<str:league_name>/', views.league_table, name='league_table'),

    path('api/teams/', views.team_list, name='team-list'),
    path('api/delete-entire-model/', views.delete_entire_model, name='delete-entire-model'),
    path('api/add/', views.add_data, name='add_data'),]