from rest_framework import serializers
import base64
from .models import Product, ProductCharacteristic, CartProduct
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
        format = product.image.path.split(".")[-1]
        img = open(product.image.path, "rb")
        data = img.read()
        return f"data:image/{format};base64,{base64.b64encode(data).decode('utf-8')}"


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    #  client = PAOSUserSerializer()
    class Meta:
        model = CartProduct
        fields = ["id",  "product"]
