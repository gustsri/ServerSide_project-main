from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    description = models.TextField()
    stock_quantity = models.IntegerField(default=0)
    categories = models.ManyToManyField("category.Category")  # Many-to-Many "app_label.ModelName"
    
    def __str__(self):
        return self.name
    
    def get_total_quantity(self):
        return sum(lot.quantity for lot in self.lots.all())  