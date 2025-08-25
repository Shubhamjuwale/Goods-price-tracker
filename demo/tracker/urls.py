from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('review/', views.review, name='review'),
    path('edit/', views.edit_watchlist, name='edit_watchlist'),
]
