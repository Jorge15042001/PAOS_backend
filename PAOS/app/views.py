
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
        products = ProductSerializer(Product.objects.filter(deleted = False), many=True).data
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
        print(product_id)
        product:Product = self.get_product(product_id)
        if not product:
            return Response({"success": False,
                             "error": "could not find product id"},
                            status=status.HTTP_404_NOT_FOUND)
        new_data = request.data
        if new_data.get("name"):
            product.name = new_data["name"]
        if new_data.get("price"):
            product.price = new_data["price"]
        if new_data.get("available"):
            product.available = new_data["available"]
        if new_data.get("deleted"):
            product.deleted = new_data["deleted"]

        try:
            product.save()
        except :
            return Response({"success": False,
                             "error": "Failed to save updated values"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, "product":ProductSerializer(product).data},
                        status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        product = self.get_product(product_id)
        if not product:
            return Response({"success": False,
                             "error": "could not find product id"},
                            status=status.HTTP_404_NOT_FOUND)
        product.deleted = True
        product.save()
        return Response({"success": True, "product":ProductSerializer(product).data},
                        status=status.HTTP_200_OK)
