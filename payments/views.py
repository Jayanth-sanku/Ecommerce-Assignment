import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if request.method == 'POST':
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Your Cart Total',
                    },
                    'unit_amount': int(cart.total_price() * 100),  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payment-success/'),
            cancel_url=request.build_absolute_uri('/payment-cancel/'),
            client_reference_id=request.user.id,  
        )

        return redirect(session.url, code=303)

    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'cart': cart,
    }
    return render(request, 'checkout.html', context)

@login_required
def payment_success(request):
    cart = Cart.objects.get(user=request.user)
    
    
    total_price = sum(item.subtotal() for item in cart.items.all())
    
    
    payment_intent = request.GET.get('payment_intent')  
    
    
    order = Order.objects.create(
        user=request.user,
        payment_intent=payment_intent,
        total_price=total_price  
    )
    
    
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            
        )
    
    
    cart.items.all().delete()

    return render(request, 'payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'payment_cancel.html')
