from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    deleted = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

class ProductCharacteristic(models.Model):
    value = models.CharField(max_length=100)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="characteristics")
