from django.contrib import admin

from .models import Product, ProductCharacteristic, ProductCategory, OrderStatus, OrderProduct, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCharacteristic)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(OrderStatus)

