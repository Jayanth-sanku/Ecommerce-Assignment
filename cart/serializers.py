from rest_framework import serializers
from .models import Cart, CartItem, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image']  

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())
