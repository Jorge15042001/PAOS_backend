from django.urls import path

from . import views

urlpatterns = [
    path("product/", views.ProductAPI.as_view(), name="product"),
    path("product/<int:product_id>", views.ProductDetailAPI.as_view(),
         name="product_deltail"),
    path("characteristic/", views.ProductCharacteristicAPI.as_view(),
         name="product_characteristic"),
    path("characteristic/<int:characteristic_id>", views.ProductCharacteristicDetailAPI.as_view(),
         name="product_characteristic_detail"),
]
