from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
   path("login/", views.login_view, name="login"),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path("search-products/", views.search_products, name="search_products"),
    path('review/', views.review, name='review'),
    path("edit_watchlist/", views.edit_watchlist, name="edit_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
]
