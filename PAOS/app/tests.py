#  from django.test import TestCase

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


from .models import OrderStatus
from accounts.models import PAOSUser
# Create your tests here.

image_base64 = " data:image/jpeg;base64,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"


class PaosBaseTestCase(APITestCase):
    def setUp(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "Jorge",
                "last_name": "Vulgarin",
                "email": "jvulgari@espol.edu.ec",
                "password1": "jvulgari",
                "password2": "jvulgari"}
        res = self.client.post(url, data, format="json").json()
        assert res["success"]


class ProductTest(PaosBaseTestCase):
    def test_create_product(self):
        url = reverse("product")
        data = {"name": "Hamburguesa", "price": 4.00,
                "characteristics": [],
                "category": None, "image": image_base64}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], True)

    def test_create_product_with_characteristics(self):
        url = reverse("product")
        data = {"name": "Hamburguesa", "price": 4.00,
                "characteristics": [{"value": "queso doble"}, {"value": "huevo frito"}],
                "category": None, "image": image_base64}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], True)
        self.assertEqual(len(response["product"]["characteristics"]), 2)

    def test_no_name(self):
        url = reverse("product")
        data = {"price": 4.00,
                "characteristics": [],
                "category": None, "image": image_base64}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)

    def test_no_image(self):
        url = reverse("product")
        data = {"name": "Hamburguesa", "price": 4.00,
                "characteristics": [],
                "category": None}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)

    def test_no_price(self):
        url = reverse("product")
        data = {"name": "Hamburguesa",
                "characteristics": [],
                "category": None}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)

    def test_update_price_no_credentials(self):
        url = reverse("product")
        data = {"name": "Hamburguesa", "price": 4.00,
                "characteristics": [],
                "category": None, "image": image_base64}
        response1 = self.client.post(url, data, format="json").json()
        product_id = response1["product"]["id"]

        update_data = {"price": 5.00}
        response2 = self.client.put(
            f"{url}{product_id}/", update_data, format="json")

        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_price(self):

        r = self.client.login(username="jvulgari", password="jvulgari")

        url = reverse("product")
        data = {"name": "Hamburguesa", "price": 4.00,
                "characteristics": [],
                "category": None, "image": image_base64}
        response1 = self.client.post(url, data, format="json").json()
        product_id = response1["product"]["id"]

        update_data = {"price": 5.00}
        response2 = self.client.put(
            f"{url}{product_id}/", update_data, format="json").json()
        new_price = response2["product"]["price"]

        self.assertEqual(response2["success"], True)
        self.assertEqual(new_price, 5)


class ProductCharacteristicsTest(PaosBaseTestCase):
    def setUp(self):
        PaosBaseTestCase.setUp(self)
        url = reverse("product")
        data = {"name": "Hamburguesa", "price": 4.00,
                "characteristics": [{"value": "queso doble"}, {"value": "huevo frito"}],
                "category": None, "image": image_base64}
        response = self.client.post(url, data, format="json").json()
        assert response["success"]

        self.product = response["product"]

        login_success = self.client.login(
            username="jvulgari", password="jvulgari")
        assert login_success

    def test_get_caracteristics(self):
        for i, characteristic in enumerate(self.product["characteristics"]):
            url = reverse("product_characteristic_detail", kwargs={
                          "characteristic_id": characteristic["id"]})
            res = self.client.get(url).json()
            self.assertEquals(res["success"], True)

    def test_update_characteristic(self):
        url = reverse("product_characteristic_detail", kwargs={
                      "characteristic_id": self.product["characteristics"][0]["id"]})

        new_name = {"value": "un solo queso"}
        res = self.client.put(url, new_name, format="json").json()
        self.assertEquals(res["success"], True)
        res2 = self.client.get(url).json()
        self.assertEquals(res2["success"], True)
        self.assertEquals(res2["characteristic"]["value"], "un solo queso")

    def test_delete_characteristic(self):
        url = reverse("product_characteristic_detail", kwargs={
                      "characteristic_id": self.product["characteristics"][0]["id"]})
        res = self.client.delete(url).json()
        self.assertEquals(res["success"], True)
        res2 = self.client.get(url).json()
        self.assertEquals(res2["success"], False)


class PaosTestCaseWithProducts(PaosBaseTestCase):
    def setUp(self):
        PaosBaseTestCase.setUp(self)

        login_success = self.client.login(
            username="jvulgari", password="jvulgari")
        assert login_success

        create_product_url = reverse("product")
        products = [
            {"name": "Hamburguesa", "price": 4.00,
             "characteristics": [{"value": "queso doble"}, {"value": "huevo frito"}],
             "category": None, "image": image_base64},
            {"name": "Papi pollo", "price": 3.00,
             "characteristics": [{"value": "doble presa"}, {"value": "papas frescas"}],
             "category": None, "image": image_base64},
            {"name": "Salchi papa", "price": 2.00,
             "characteristics": [{"value": "4 chorizos"}],
             "category": None, "image": image_base64},
            {"name": "Pan de yuca", "price": 4.00,
             "characteristics": [],
             "category": None, "image": image_base64},
        ]
        responses = list(map(lambda p: self.client.post(
            create_product_url, p, format="json").json(), products))
        assert all(map(lambda res: res["success"], responses))

        self.products = list(map(lambda res: res["product"], responses))
#
#
#  class CartTestCase(PaosTestCaseWithProducts):
#      def setUp(self):
#          PaosTestCaseWithProducts.setUp(self)
#
#      def test_add_to_cart(self):
#          url = reverse("product_cart")
#          data = {
#              "product": self.products[0]["id"],
#              "quantity": 10
#          }
#          res = self.client.post(url, data, format="json").json()
#          self.assertEquals(res["success"], True)
#
#          res2 = self.client.get(url).json()
#          self.assertEquals(res2["success"], True)
#          self.assertEquals(len(res2["cart"]), 1)
#
#      def test_add_to_cart_not_valid_quantity(self):
#          url = reverse("product_cart")
#          data = {
#              "product": self.products[0]["id"],
#              "quantity": -10
#          }
#          res = self.client.post(url, data, format="json").json()
#          self.assertEquals(res["success"], False)
#
#      def test_add_to_cart_add_to_cart_already_added_products(self):
#          url = reverse("product_cart")
#          data = {
#              "product": self.products[0]["id"],
#              "quantity": 2
#          }
#          res = self.client.post(url, data, format="json").json()
#          self.assertEquals(res["success"], True)
#
#          res2 = self.client.post(url, data, format="json").json()
#          self.assertEquals(res2["success"], True)
#
#          res3 = self.client.get(url).json()
#          self.assertEquals(res3["success"], True)
#          self.assertEquals(res3["cart"][0]["quantity"], 4)
#
#      def test_diminish_quantity(self):
#          url = reverse("product_cart")
#          data = {
#              "product": self.products[0]["id"],
#              "quantity": 2
#          }
#          res = self.client.post(url, data, format="json").json()
#          self.assertEquals(res["success"], True)
#
#          data2 = {
#              "product": self.products[0]["id"],
#              "quantity": -1
#          }
#          res2 = self.client.post(url, data2, format="json").json()
#          self.assertEquals(res2["success"], True)
#
#          res3 = self.client.get(url).json()
#          self.assertEquals(res3["success"], True)
#          self.assertEquals(res3["cart"][0]["quantity"], 1)
#
#      def test_diminish_quantity_remove_at_0(self):
#          url = reverse("product_cart")
#          data = {
#              "product": self.products[0]["id"],
#              "quantity": 2
#          }
#          res = self.client.post(url, data, format="json").json()
#          self.assertEquals(res["success"], True)
#
#          data2 = {
#              "product": self.products[0]["id"],
#              "quantity": -2
#          }
#          res2 = self.client.post(url, data2, format="json").json()
#          self.assertEquals(res2["success"], True)
#          self.assertEquals(res2["product"], None)
#
#          res3 = self.client.get(url).json()
#          self.assertEquals(res3["success"], True)
#          self.assertEquals(len(res3["cart"]), 0)
#
#


class PaosTestCaseWithCart(PaosTestCaseWithProducts):
    def setUp(self):
        PaosTestCaseWithProducts.setUp(self)

        url = reverse("product_cart")
        data = {
            "product": self.products[0]["id"],
            "quantity": 2
        }
        res = self.client.post(url, data, format="json").json()
        assert res["success"]

        data2 = {
            "product": self.products[0]["id"],
            "quantity": 2
        }

        res2 = self.client.post(url, data2, format="json").json()
        assert res2["success"]

        res3 = self.client.get(url).json()
        assert res3["success"]

        self.cart = res3["cart"]


class CartDetailTestCase(PaosTestCaseWithCart):
    def test_get(self):
        url = reverse("product_cart_detail", kwargs={
                      "item_id": self.cart[0]["id"]})
        res = self.client.get(url).json()
        self.assertEquals(res["success"], True)
        self.assertEquals(res["cart_item"]["id"], self.cart[0]["id"])

    def test_delete(self):
        url = reverse("product_cart_detail", kwargs={
                      "item_id": self.cart[0]["id"]})
        res = self.client.delete(url).json()
        self.assertEquals(res["success"], True)

        res2 = self.client.get(url).json()
        self.assertEquals(res2["success"], False)


class OrderCartTest(PaosTestCaseWithCart):
    def setUp(self):
        PaosTestCaseWithProducts.setUp(self)

        OrderStatus.objects.create(name="PENDING").save()
        OrderStatus.objects.create(name="CANCELLED").save()
        OrderStatus.objects.create(name="DELIVERED").save()

    def test_buy_cart(self):
        url = reverse("order_cart")
        data = {"delivery_address": "36 y portete"}
        res = self.client.post(url, data, format="json").json()
        self.assertEquals(res["success"], True)

        url2 = reverse("product_cart")
        res2 = self.client.get(url2).json()
        self.assertEquals(res2["success"], True)
        self.assertEquals(len(res2["cart"]), 0)


class OderDetailTest(PaosTestCaseWithCart):
    def setUp(self):
        PaosTestCaseWithProducts.setUp(self)

        OrderStatus.objects.create(name="PENDING").save()
        OrderStatus.objects.create(name="CANCELLED").save()
        OrderStatus.objects.create(name="DELIVERED").save()

    def test_order_not_found(self):
        url = reverse("order_detail", kwargs={"order_id": 10})
        data = {"state": "DELIVERED"}

        res = self.client.put(url, data, format="json").json()
        self.assertEquals(res["success"], False)

    def test_order_no_state(self):
        pass
        url = reverse("order_detail", kwargs={"order_id": 10})
        data = {}

        res = self.client.put(url, data, format="json").json()
        self.assertEquals(res["success"], False)


class TestOrderDelivereAPI(PaosTestCaseWithCart):
    def setUp(self):
        PaosTestCaseWithProducts.setUp(self)

        OrderStatus.objects.create(name="PENDING").save()
        OrderStatus.objects.create(name="CANCELLED").save()
        OrderStatus.objects.create(name="DELIVERED").save()

        #  self.client.logout()

    def test_mark_order_as_delivered(self):
        url = reverse("order_deliverer", kwargs={"order_id": 10})
        data = {"state": "DELIVERED"}

        res = self.client.put(url, data, format="json")
        print(res)
        print(res.status_code)
        res = res.json()
        print(res)
        self.assertEquals(res["success"], False)


#  class OrderTestCase(APITestCase):

#      def setUp(self):
#          url = reverse("api_signup")
#          data = {"username": "jvulgari",
#                  "first_name": "Jorge",
#                  "last_name": "Vulgarin",
#                  "email": "jvulgari@espol.edu.ec",
#                  "password1": "jvulgari",
#                  "password2": "jvulgari"}
#          self.client.post(url, data, format="json").json()
