from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('new/', views.new_entry, name='new_entry'),
    path('edit/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:pk>/', views.delete_entry, name='delete_entry'),
    path('search/', views.search_entries, name='search_entries'),
    path('profile/', views.profile, name='profile'),
    path('stats/', views.get_stats, name='get_stats'),
]