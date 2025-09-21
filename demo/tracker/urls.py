from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('watchlist/add/<int:product_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path("login/", views.login_view, name="login"),
    path('signup/', views.signup, name='signup'), 
    path("search-products/", views.search_products, name="search_products"),
    path('review/', views.review, name='review'),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/create/", views.create_watchlist, name="create_watchlist"),
    path("watchlist/remove/<int:watchlist_id>/", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist/<int:watchlist_id>/remove/<int:product_id>/", views.remove_item, name="remove_item_from_watchlist"),
    path("watchlist/<int:watchlist_id>/add/<int:product_id>/", views.add_item, name="add_item_to_watchlist"),

    # AJAX
    path("watchlist/ajax/show_more/<int:watchlist_id>/", views.ajax_show_more_watchlist_items, name="ajax_show_more_watchlist_items"),
    path("watchlist/ajax/add_item/", views.ajax_add_to_watchlist, name="ajax_add_to_watchlist"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
]
