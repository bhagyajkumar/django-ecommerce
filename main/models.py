from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    thumbnail = models.ImageField(upload_to="product_images/")
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart")


class ProductOrder(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")
