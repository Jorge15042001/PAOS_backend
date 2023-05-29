
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework import status
from rest_framework import permissions

from .serializers import ProductSerializer, ProductCharacteristicSerializer
from .models import Product, ProductCharacteristic

# Create your views here.


class ProductAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = ProductSerializer(
            Product.objects.filter(deleted=False), many=True).data
        return Response({"success": True, "products": products})

    def post(self, request):

        data = {
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'characteristics': request.data.get('characteristics')
        }
        product = ProductSerializer(data=data)

        if product.is_valid():
            p = product.save()
            return Response({"success": True,
                             "product": ProductSerializer(p).data},
                            status=status.HTTP_200_OK)
        return Response({"success": False, "errors": product.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_product(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_id):
        product = ProductSerializer(self.get_product(product_id)).data
        if not product:
            return Response({"success": False,
                             "error": "could not find product id"},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({"success": True, "product": product},
                        status=status.HTTP_200_OK)

    def put(self, request, product_id):
        product: Product = self.get_product(product_id)
        if not product:
            return Response({"success": False,
                             "error": "could not find product id"},
                            status=status.HTTP_404_NOT_FOUND)
        new_data = request.data

        if "name" in new_data:
            product.name = new_data["name"]
        if "price" in new_data:
            product.price = new_data["price"]
        if "available" in new_data:
            print("setting available")
            product.available = new_data["available"]
        if "deleted" in new_data:
            product.deleted = new_data["deleted"]

        try:
            product.save()
        except:
            return Response({"success": False,
                             "error": "Failed to save updated values"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True,
                         "product": ProductSerializer(product).data},
                        status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        product = self.get_product(product_id)
        if not product:
            return Response({"success": False,
                             "error": "could not find product id"},
                            status=status.HTTP_404_NOT_FOUND)
        product.deleted = True
        product.save()

        return Response({"success": True,
                         "product": ProductSerializer(product).data},
                        status=status.HTTP_200_OK)


class ProductCharacteristicAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        characteristic = ProductCharacteristicSerializer(data=request.data)
        print(characteristic)
        print(characteristic.is_valid())
        if characteristic.is_valid():
            c = characteristic.save()
            return Response({"success": True, "characteristic":
                             ProductCharacteristicSerializer(c).data},
                            status=status.HTTP_200_OK)
        return Response({"success": False, "errors": characteristic.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class ProductCharacteristicDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_characteristic(self, characteristic_id):
        try:
            return ProductCharacteristic.objects.get(id=characteristic_id)
        except ProductCharacteristic.DoesNotExist:
            return None

    def get(self, request, characteristic_id):
        characteristic = self.get_characteristic(characteristic_id)

        if not characteristic:
            return Response({"success": False, "error":
                             "could not find product characteristic id"},
                            status=status.HTTP_404_NOT_FOUND)
        serialized = ProductCharacteristicSerializer(characteristic).data

        return Response({"success": True, "characteristic": serialized},
                        status=status.HTTP_200_OK)

    def put(self, request, characteristic_id):
        characteristic = self.get_characteristic(characteristic_id)

        if not characteristic:
            return Response({"success": False, "error":
                             "could not find product characteristic id"},
                            status=status.HTTP_404_NOT_FOUND)
        if "value" in request.data:
            characteristic.value = request.data["value"]
        try:
            characteristic.save()
        except:
            return Response({"success": False,
                             "error": "Failed to save updated values"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, "product":
                         ProductCharacteristicSerializer(characteristic).data},
                        status=status.HTTP_200_OK)

    def delete(self, request, characteristic_id):
        characteristic = self.get_characteristic(characteristic_id)

        if not characteristic:
            return Response({"success": False, "error":
                             "could not find product characteristic id"},
                            status=status.HTTP_404_NOT_FOUND)

        characteristic.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
        pass
