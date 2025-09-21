from django.db import models
from django.conf import settings  

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(max_length=100)
    tag = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  

    def __str__(self):
        return self.name

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    products = models.ManyToManyField(Product)

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    price = models.FloatField()
    price_date = models.DateField(null=False, blank=False)

    class Meta:
        unique_together = ('product', 'price_date')  

    def __str__(self):
     if self.price_date:
        return f"{self.product.name} - ₹{self.price} on {self.price_date.strftime('%Y-%m-%d')}"
     return f"{self.product.name} - ₹{self.price} (no date)"