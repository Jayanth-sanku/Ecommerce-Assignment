# adminapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm  
from catalog.models import Product  
from orders.models import Order  
from django.contrib.auth import logout

@login_required
def admin_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    product_form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added/updated successfully.')
            return redirect('admin_dashboard')

    context = {
        'products': products,
        'orders': orders,
        'product_form': product_form,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def admin_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)

    context = {'product_form': form}
    return render(request, 'edit_product.html', context)

@login_required
def admin_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('admin_dashboard')

@login_required
def admin_view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'adminapp/order_detail.html', context)


@login_required
def admin_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('admin_dashboard')  
    else:
        form = ProductForm()

    context = {'product_form': form}
    return render(request, 'edit_product.html', context)

def custom_logout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/auth/login/')