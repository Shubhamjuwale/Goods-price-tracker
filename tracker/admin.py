from django.contrib import admin
from .models import Product, Price, Review, Watchlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit']
    search_fields = ['name', 'category']


admin.site.register(Price)
admin.site.register(Review)
admin.site.register(Watchlist)
