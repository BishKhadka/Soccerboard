from django.urls import path, include
from soccerboard import views

urlpatterns = [
    path('', views.home, name="home"),
    path('quiz/', views.quiz, name = 'quiz'),
    path('search_page/<str:league>', views.search_page, name='search_page'),
    path('stats/<str:league_name>/<str:team_name>/', views.stats, name='stats'),
    path('league_table/<str:league_name>/', views.league_table, name='league_table'),
    path('contact', views.contact, name = "contact"),
    path('about', views.acknowledgement, name = "acknowledgement"),
    path('api/teams/', views.team_list, name='team-list'),
    path('api/delete-entire-model/', views.delete_entire_model, name='delete-entire-model'),
    path('api/add/', views.add_data, name='add-data'),
    path('api/all-data/', views.all_data, name='all-data'),
    ]