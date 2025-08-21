from django.contrib import admin
from .models import Product, Price, Review, Watchlist
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit']
    search_fields = ['name', 'category']

admin.site.register(Price)
admin.site.register(Review)
admin.site.register(Watchlist)
admin.site.register(User)
