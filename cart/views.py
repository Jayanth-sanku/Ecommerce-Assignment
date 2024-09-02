from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@login_required
def cart_page(request):
    # Get the cart for the current user
    cart = Cart.objects.filter(user=request.user).first()

    # If no cart exists for the user, create one
    if not cart:
        cart = Cart.objects.create(user=request.user)

    context = {
        'cart': cart,
        'cart_items': cart.items.all(),  # Fetch all items in the cart
    }

    return render(request, 'cart_page.html', context)


@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_count = cart.items.count()  # Use the related_name 'items'
    else:
        cart_count = 0

    return JsonResponse({'cart_count': cart_count})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def cart_item_add(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return HttpResponse(status=204)  # No Content


@login_required
@require_http_methods(["POST"])
def cart_item_update(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity = quantity
    cart_item.save()
    return JsonResponse({'message': 'Cart item updated'})


@login_required
@require_http_methods(["POST"])
def cart_item_delete(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return JsonResponse({'message': 'Cart item deleted'})
