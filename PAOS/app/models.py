from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    deleted = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    imgage = models.ImageField(upload_to="product_images", default="/etc/images/no_image.png")


class ProductCharacteristic(models.Model):
    value = models.CharField(max_length=100)
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="characteristics")


class CartProduct(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product")
    client = models.ForeignKey(
        "accounts.PAOSUser", on_delete=models.CASCADE, related_name="client")
