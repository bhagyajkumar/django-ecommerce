from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_page, name="homepage"),
    path("add-to-cart", views.add_to_cart),
    path("cart", views.view_cart, name="cart_page",),
    path("cart/increment/<product_id>",
         views.increment_item, name="increment_item"),
    path("cart/decrement/<product_id>",
         views.decrement_item, name="decrement_item"),
    path("checkout", views.checkout, name="checkout"),
    path("add-data/", views.set_placeholder_data)
]
