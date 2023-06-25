from rest_framework import serializers
from .models import Product, ProductCharacteristic, CartProduct
from drf_extra_fields.fields import Base64ImageField


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = ["id", "value", ]


class ProductSerializer(serializers.ModelSerializer):
    #  image = serializers.SerializerMethodField(read_only=True)
    image=Base64ImageField(represent_in_base64=True)


    characteristics = ProductCharacteristicSerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "price", "deleted", "available",
                  "characteristics", "id", "image"]

    def create(self, validated_data):
        characteristics_data = validated_data.pop("characteristics")
        product = Product.objects.create(**validated_data)

        for characteristic_data in characteristics_data:
            ProductCharacteristic.objects.create(product=product,
                                                 **characteristic_data)
        return product


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ["id", "client", "product"]
