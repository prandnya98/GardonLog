# from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Flora(models.Model):
    f_name = models.CharField(max_length=20)
    f_description = models.TextField(max_length=200)
    f_price = models.DecimalField(max_digits=7, decimal_places=2)
    f_category = models.CharField(max_length=30)
    f_scientific_name = models.CharField(max_length=100)
    f_color = models.CharField(max_length=50)
    f_image = models.ImageField(upload_to="flora/", blank=True, null=True)

    def __str__(self):
        return self.f_name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 1 user = 1 cart
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Flora, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.f_price * self.quantity

    def __str__(self):
        return f"{self.product.f_name} (x{self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Flora, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.f_name} (x{self.quantity})"



class SupportComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"