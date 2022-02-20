import json
from django.http import Http404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Cart, Product, ProductOrder
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import stripe


def home_page(request):
    products = Product.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.get_or_create(user=request.user)[0].items.all()
        for i in cart_items:
            cart_count += i.count
    return render(request, "home.html", {"products": products, "cart_count": cart_count})


@login_required
def add_to_cart(request):
    product_id = request.GET["product_id"]
    print(product_id)
    return HttpResponse(request, "test")


def view_cart(request):
    if not request.user.is_authenticated:
        return HttpResponse("Please login to access cart")
    cart_items = Cart.objects.get(user=request.user).items.all()
    cart_count = 0
    for i in cart_items:
        cart_count += i.count
    return render(request, "cart.html", {"cart_items": cart_items, "cart_count": cart_count})


# gotta handle 404
def increment_item(request, product_id):
    user = request.user
    cart = user.cart.get()
    product = Product.objects.get(pk=product_id)
    product_order, created = ProductOrder.objects.get_or_create(
        cart=cart, product=product)
    if not created:
        product_order.count += 1
    product_order.save()
    return HttpResponseRedirect(reverse("cart_page"))


def decrement_item(request, product_id):
    user = request.user
    cart = user.cart.get()
    product = Product.objects.get(pk=product_id)
    product_order = ProductOrder.objects.get(cart=cart, product=product)
    product_order.count -= 1
    product_order.save()

    if product_order.count <= 0:
        product_order.delete()

    return HttpResponseRedirect(reverse("cart_page"))

# This view is to create some place holder data from an api


def set_placeholder_data(request):
    from django.core.files import File
    from django.http import HttpResponse
    import requests
    from io import BytesIO
    import requests

    data = requests.get("https://fakestoreapi.com/products").json()
    for d in data[0:5]:
        title = d["title"]
        price = d["price"]
        description = d["description"]
        image_url = d["image"]
        image = requests.get(image_url).content
        img = File(BytesIO(image), "rb")
        p = Product.objects.create(
            title=title, description=description, price=price, thumbnail=img)
        p.save()
    return HttpResponse("data saved")


@login_required
def checkout(request):
    cart_items = Cart.objects.get(user=request.user).items.all()
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types = ["card"],
        line_items = [{"price": item.product.stripe_price_id, "quantity": item.count} for item in cart_items],
        mode="payment",
        success_url="http://127.0.0.1:8000/payment/success",
        cancel_url = "http://127.0.0.1:8000/payment/cancel"
    )
    price = 0
    for item in cart_items:
        price += item.count * item.product.price
    # line_items = [{"price": item.product.stripe_price_id, "quantity": item.count} for item in cart_items]
    context = {
        "session_id": checkout_session.id,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "amount_rs": price
    }
    return render(request, "payment.html", context)