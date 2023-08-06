from django.db import models
from django.utils.timezone import now

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey("ProductCategory", on_delete=models.SET_NULL,
                                 related_name="category", null=True)
    price = models.FloatField()
    deleted = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="product_images",
                              default="product_images/no_image.png")


class ProductCharacteristic(models.Model):
    value = models.CharField(max_length=100)
    product = models.ForeignKey("Product", on_delete=models.CASCADE,
                                related_name="characteristics")


class CartProduct(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE,
                                related_name="product")
    quantity = models.IntegerField(default=1)
    client = models.ForeignKey("accounts.PAOSUser", on_delete=models.CASCADE,
                               related_name="client")


class OrderStatus (models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Order(models.Model):
    client = models.ForeignKey("accounts.PAOSUser", on_delete=models.CASCADE,
                               related_name="order_client")
    time = models.DateTimeField(default=now)
    state = models.ForeignKey(
        "OrderStatus", on_delete=models.SET_NULL,
        related_name="status", null=True)
    delivery_address = models.CharField(max_length=200, null=True)


class OrderProduct(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE,
                                related_name="order_product",)
    order = models.ForeignKey("Order", on_delete=models.CASCADE,
                              related_name="order_products")
