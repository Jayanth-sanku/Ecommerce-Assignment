from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_items(self):
        """Returns the total number of items in the cart."""
        return self.items.count()

    def total_price(self):
        """Returns the total price of all items in the cart."""
        return sum(item.subtotal() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"

    def subtotal(self):
        """Returns the subtotal price for this item."""
        return self.product.price * self.quantity
