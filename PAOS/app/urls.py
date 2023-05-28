from django.urls import path

from . import views

urlpatterns = [
    path("product/",views.ProductAPI.as_view(),name="product"),
    path("product/<int:product_id>",views.ProductDetailAPI.as_view(),name="product_deltail"),
]

