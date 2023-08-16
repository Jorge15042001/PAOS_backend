from django.urls import path

from . import views

urlpatterns = [
    path("api_login/",views.APILogin.as_view(),name="api_login"),
    path("api_signup/",views.APISignup.as_view(),name="api_signup")
]

