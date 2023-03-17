from django.urls import path

from .views import shop_index, groups_list, products_list, create_product, orders_list, create_order

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", products_list, name="products_list"),
    path("products/create", create_product, name="products_create"),
    path("orders/", orders_list, name="orders_list"),
    path("orders/create", create_order, name="orders_create"),
]
