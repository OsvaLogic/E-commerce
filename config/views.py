from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from products.models import Order, OrderItem
from products.views import get_clean_cart

def catalog(request):
    # Redirigimos la ruta raíz (/) al nuevo y mejorado catálogo
    return redirect('product_list')

def get_cart(request):
    return get_clean_cart(request)

def add_to_cart(request, product_id):
    # Obsoleto: la lógica del carrito ahora se maneja en products.views
    return redirect('product_list')

def remove_from_cart(request, product_id):
    return redirect('view_cart')

def cart_detail(request):
    return redirect('view_cart')

@login_required(login_url='/login/')
def checkout(request):
    cart = get_clean_cart(request)
    if not cart:
        messages.error(request, "Tu carrito está vacío. Agrega productos para comprar.")
        return redirect('product_list')
        
    # Crear la Orden maestra
    order = Order.objects.create(user=request.user, total=0)
    total = 0
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        price = product.price
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        total += price * quantity
        
    order.total = total
    order.save()
    
    # Limpiar el carrito después de comprar
    request.session['cart'] = {}
    messages.success(request, f"¡Compra confirmada! Tu orden #{order.id} ha sido registrada.")
    return redirect('product_list')