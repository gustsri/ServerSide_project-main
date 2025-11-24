from django.db import models
from product.models import Product
from decimal import Decimal
# Create your models here.

class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.id} - {self.date}"  # Modified to use self.id
    

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE ,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)#test
    quantity = models.PositiveIntegerField(default=0) # ใช้ PositiveIntegerField
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # กำหนด default เป็น Decimal

    def __str__(self):
        return f"SaleItem in Sale {self.sale.id}"
