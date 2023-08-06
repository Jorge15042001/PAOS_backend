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
    path("cart/", views.ProductCartAPI.as_view(),
         name="product_cart"),
    path("cart/<int:item_id>", views.ProductCartDetailAPI.as_view(),
         name="product_cart_detail"),
    path("order/", views.OrderAPI.as_view(), name="order"),
    path("order/<int:order_id>", views.OrderDetailAPI.as_view(), name="order_detail"),
    path("order_deliverer/<int:order_id>", views.OrderDetailAPI.as_view(), name="order_deliverer"),
    path("order_cart/", views.OrderCartAPI.as_view(), name="order_cart"),

]
