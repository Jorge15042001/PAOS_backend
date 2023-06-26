
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework import status
from rest_framework import permissions

from .serializers import ProductSerializer, ProductCharacteristicSerializer, CartProductSerializer
from .models import Product, ProductCharacteristic, CartProduct

# Create your views here.


class ProductAPI(APIView):

    def get(self, request):
        products = ProductSerializer(
            Product.objects.filter(deleted=False), many=True).data
        return Response({"success": True, "products": products})

    def post(self, request):

        data = {
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'category': request.data.get('category'),
            'characteristics': request.data.get('characteristics'),
            'image': request.data.get('image')
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
        except Exception as e:
            print(e)
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


class ProductCartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_products = CartProductSerializer(
            CartProduct.objects.filter(client=request.user), many=True).data
        return Response({"success": True, "cart": cart_products})

    def post(self, request):

        data = {
            'client': request.user.id,
            'product': request.data.get('product'),
            'quantity': request.data.get('quantity'),
        }
        try:
            # if Product already in cart
            cart_product = CartProduct.objects.get(client=data["client"],
                                                   product=data["product"])
            cart_product.quantity += data["quantity"]
            cart_product.save()
            return Response({"success": True,
                             "product": CartProductSerializer(cart_product).data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        # if Product not in cart
        cart_product = CartProductSerializer(data=data)

        if cart_product.is_valid():
            saved_cart_product = cart_product.save()
            return Response({"success": True,
                             "product": CartProductSerializer(saved_cart_product).data},
                            status=status.HTTP_200_OK)

        return Response({"success": False, "errors": cart_product.errors},
                        status=status.HTTP_400_BAD_REQUEST)

class ProductCartDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart_item(self, item_id):
        try:
            return CartProduct.objects.get(id=item_id)
        except CartProduct.DoesNotExist:
            return None


    def get(self, request, item_id):
        cart_product = self.get_cart_item(item_id)
        if not cart_product:
            return Response({"success": False, "error":
                             "could not find cart item"},
                            status=status.HTTP_404_NOT_FOUND)
        serialized = CartProductSerializer(cart_product).data

        return Response({"success": True, "cart_item": serialized},
                        status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        cart_item = self.get_cart_item(item_id)

        if not cart_item:
            return Response({"success": False, "error":
                             "could not find cart item id"},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
