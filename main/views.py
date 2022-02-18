from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Cart, Product, ProductOrder
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

def home_page(request):
    products = Product.objects.all()
    cart_items = Cart.objects.get_or_create(user=request.user)[0].items.all()
    cart_count = 0
    for i in cart_items:
        cart_count += i.count
    return render(request, "main/home.html", {"products": products, "cart_count": cart_count})


@login_required
def add_to_cart(request):
    product_id = request.GET["product_id"]
    print(product_id)
    return HttpResponse(request, "test")


def view_cart(request):
    cart_items = Cart.objects.get(user=request.user).items.all()
    cart_count = 0
    for i in cart_items:
        cart_count += i.count
    return render(request, "main/cart.html", {"cart_items": cart_items, "cart_count": cart_count})


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
    for d in data:
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


# def checkout(request):
#     cart_items = Cart.objects.get(user=request.user).items.all()
#     amount = 0
#     for i in cart_items:
#         amount += i.product.price * i.count
#     amount = int(amount * 100)
#     currency = "INR"
#     razorpay_order = razorpay_client.order.create(
#         {
#             "amount": amount,
#             "currency": currency,
#             "payment_capture": "0",
#         }
#     )
#     razorpay_order_id = razorpay_order['id']
#     callback_url = "paymenthandler/"

#     context = {
#         "razorpay_order_id": razorpay_order_id,
#         "razorpay_merchant_key": settings.RAZOR_KEY_ID,
#         "razorpay_amount": amount,
#         "currency": "INR",
#         "callback_url": callback_url,
#         "amount_rs": amount / 100
#     }

#     return render(request, "main/payment.html", context)
