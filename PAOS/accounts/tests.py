#  from django.test import TestCase
#  from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


from .models import PAOSUser

# Create your tests here.


class UserCreationTest(APITestCase):
    def test_pass_missing(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "Jorge",
                "last_name": "Vulgarin",
                "email": "jvulgari@espol.edu.ec",
                "password1": "jvulgari",
                "password2": ""}

        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)

    def test_pass_missing2(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "Jorge",
                "last_name": "Vulgarin",
                "email": "jvulgari@espol.edu.ec",
                "password1": "",
                "password2": "jvulgari"}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)

    def test_no_email(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "Jorge",
                "last_name": "Vulgarin",
                "password1": "jvulgari",
                "password2": "jvulgari"}
        response = self.client.post(url, data, format="json").json()
        print(response)
        self.assertEqual(response["success"], False)

    def test_password_mismatch(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "Jorge",
                "last_name": "Vulgarin",
                "email": "jvulgari@espol.edu.ec",
                "password1": "J#orge1504",
                "password2": "Jorge1504"}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)

    def test_normal_user_signup(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "Jorge",
                "last_name": "Vulgarin",
                "email": "jvulgari@espol.edu.ec",
                "password1": "jvulgari",
                "password2": "jvulgari"}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], True)

    def test_repeted_username(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "jorge",
                "last_name": "vulgarin",
                "email": "jvulgari@espol.edu.ec",
                "password1": "jvulgari",
                "password2": "jvulgari"}
        response_1 = self.client.post(url, data, format="json").json()
        response_2 = self.client.post(url, data, format="json").json()

        self.assertEqual(response_1["success"], True)
        self.assertEqual(response_2["success"], False)


class UserLogin(APITestCase):
    def setUp(self):
        url = reverse("api_signup")
        data = {"username": "jvulgari",
                "first_name": "Jorge",
                "last_name": "Vulgarin",
                "email": "jvulgari@espol.edu.ec",
                "password1": "jvulgari",
                "password2": "jvulgari"}
        self.client.post(url, data, format="json").json()

    def test_login(self):
        url = reverse("api_login")
        data = {"username": "jvulgari",
                "password": "jvulgari"}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], True)

    def test_wrong_password(self):
        url = reverse("api_login")
        data = {"username": "jvulgari",
                "password": "jvulgar"}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)
        self.assertEqual(response["error"], "Wrong username and/or password")

    def test_wrong_username(self):
        url = reverse("api_login")
        data = {"username": "julgari",
                "password": "jvulgari"}
        response = self.client.post(url, data, format="json").json()
        self.assertEqual(response["success"], False)
        self.assertEqual(response["error"], "Wrong username and/or password")
