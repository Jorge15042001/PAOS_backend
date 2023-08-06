from rest_framework import serializers
import base64
from .models import Product, ProductCharacteristic, CartProduct, Order
from accounts.models import PAOSUser
from accounts.serializers import PAOSUserSerializer
from drf_extra_fields.fields import Base64ImageField


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = ["id", "value", ]


class ProductSerializer(serializers.ModelSerializer):
    image_base64 = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    characteristics = ProductCharacteristicSerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "price", "deleted", "available", "category",
                  "characteristics", "id", "image", "image_base64"]

    def create(self, validated_data):
        characteristics_data = validated_data.pop("characteristics")
        product = Product.objects.create(**validated_data)

        for characteristic_data in characteristics_data:
            ProductCharacteristic.objects.create(product=product,
                                                 **characteristic_data)
        return product

    def get_image_base64(self, product):
        format = product.image.path.split(".")[-1]  # file format
        img = open(product.image.path, "rb")
        data = img.read()
        base64_str = base64.b64encode(data).decode('utf-8')
        return f"data:image/{format};base64,{base64_str}"


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    client = PAOSUserSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ["id",  "product", "client", "quantity"]

    def to_internal_value(self, data):
        ret = {
            "product": Product(id=data["product"]),
            "client": PAOSUser(id=data["client"]),
            "quantity": data["quantity"],
        }
        return ret

    #  def create(self, validated_data):
    #      print(validated_data)


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id",  "product"]


class OrderSerializer(serializers.ModelSerializer):
    client = PAOSUserSerializer(read_only=True)
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "client", "time", "state",
                  "delivery_address", "order_products"]

    #  def create(self, validated_data):
    #      characteristics_data = validated_data.pop("characteristics")
    #      product = Product.objects.create(**validated_data)
    #
    #      for characteristic_data in characteristics_data:
    #          ProductCharacteristic.objects.create(product=product,
    #                                               **characteristic_data)
        #  return product
    #  def to_internal_value(self, data):
    #      ret = {
    #          "product": Product(id=data["product"]),
    #          "client": PAOSUser(id=data["client"]),
    #          "quantity": data["quantity"],
    #      }
    #      return ret
