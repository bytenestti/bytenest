from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('projects/', views.projects_view, name='projects'),
    path('analytics/', views.analytics_view, name='analytics'),
]
