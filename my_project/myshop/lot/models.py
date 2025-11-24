from django.db import models
from product.models import Product

# Create your models here.
class Lot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='lots')
    import_date = models.DateField()
    expiry_date = models.DateField()
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Lot {self.product.name} (Import: {self.import_date}) (Expiry: {self.expiry_date})"
    
