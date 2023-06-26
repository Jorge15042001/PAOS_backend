from django.db import models

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
