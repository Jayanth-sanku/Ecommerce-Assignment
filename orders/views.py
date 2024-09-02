from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # Example of creating an order with hardcoded data
        data = request.data
        total_price = sum(item['price'] * item['quantity'] for item in data['items'])
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in data['items']:
            OrderItem.objects.create(
                order=order,
                product_id=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
