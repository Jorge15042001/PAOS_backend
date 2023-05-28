
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
        products = ProductSerializer(Product.objects.all(), many=True).data
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
