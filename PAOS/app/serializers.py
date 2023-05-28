from rest_framework import serializers
from .models import Product, ProductCharacteristic


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = ["value"]


class ProductSerializer(serializers.ModelSerializer):
    characteristics = ProductCharacteristicSerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "price", "deleted", "available", "characteristics"]

    def create(self, validated_data):
        characteristics_data = validated_data.pop("characteristics")
        product = Product.objects.create(**validated_data)

        for characteristic_data in characteristics_data:
            characteristic = ProductCharacteristic.objects.create(product = product, **characteristic_data)
            
        return product
