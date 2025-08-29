from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
   path("login/", views.login_view, name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('review/', views.review, name='review'),
    path("edit_watchlist/", views.edit_watchlist, name="edit_watchlist"),

]
