from django.contrib import admin
from datetime import date
from .models import Product, Price, Review, Watchlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'price']
    search_fields = ['name', 'category']
    actions = ['save_prices_to_history']

    def save_prices_to_history(self, request, queryset):
        """
        Save current prices of all products into the Price history table.
        Each product gets one price entry for the 1st of the current month.
        """
        today = date.today().replace(day=1)

        for product in Product.objects.all():
            Price.objects.update_or_create(
                product=product,
                price_date=today,
                defaults={'price': product.price}
            )

        self.message_user(request, " Current prices saved to Price history!")

    save_prices_to_history.short_description = "Save current prices to Price history"


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'price_date']
    list_filter = ['price_date']
    search_fields = ['product__name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'date']
    search_fields = ['user__username', 'comment']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    search_fields = ['name', 'user__username']
    filter_horizontal = ['products']  