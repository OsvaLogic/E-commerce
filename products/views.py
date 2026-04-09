from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category
from .forms import ProductForm

# Función de test para verificar si un usuario es administrador (staff)
def is_admin(user):
    return user.is_staff

# Función auxiliar para limpiar el carrito de productos eliminados
def get_clean_cart(request):
    cart = request.session.get('cart', {})
    if cart:
        valid_ids = [str(i) for i in Product.objects.filter(id__in=cart.keys()).values_list('id', flat=True)]
        cart = {k: v for k, v in cart.items() if k in valid_ids}
        request.session['cart'] = cart
    return cart

def product_list(request):
    products = Product.objects.all()
    
    # Cargar datos automáticamente si el inventario está vacío
    if not products.exists():
        cat_audio, _ = Category.objects.get_or_create(name="AUDIO")
        cat_perif, _ = Category.objects.get_or_create(name="PERIFÉRICOS")
        cat_moni, _ = Category.objects.get_or_create(name="MONITORES")
        cat_mueb, _ = Category.objects.get_or_create(name="MUEBLES")
        cat_acc, _ = Category.objects.get_or_create(name="ACCESORIOS")

        products_data = [
            {"name": "HEADSET HYPERION X", "cat": cat_audio, "price": 120000, "img": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=500&q=80"},
            {"name": "TECLADO MECÁNICO K-70", "cat": cat_perif, "price": 185000, "img": "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=500&q=80"},
            {"name": "MOUSE GAMER G-PRO", "cat": cat_perif, "price": 95000, "img": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?auto=format&fit=crop&w=500&q=80"},
            {"name": "MONITOR CURVO 144HZ", "cat": cat_moni, "price": 290000, "img": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80"},
            {"name": "SILLA GAMER OMEGA", "cat": cat_mueb, "price": 150000, "img": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?auto=format&fit=crop&w=500&q=80"},
            {"name": "MOUSEPAD RGB XXL", "cat": cat_acc, "price": 35000, "img": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=500&q=80"},
        ]

        for p in products_data:
            Product.objects.create(
                name=p["name"], category=p["cat"], price=p["price"], stock=15, description="Producto autogenerado de muestra.", image_url=p["img"]
            )
        products = Product.objects.all() # Refrescar la lista de productos

    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
        
    cart = get_clean_cart(request)
    cart_count = sum(cart.values())
        
    return render(request, 'products/product_list.html', {
        'products': products,
        'cart_count': cart_count
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart = get_clean_cart(request)
    cart_count = sum(cart.values())
    return render(request, 'products/product_detail.html', {'product': product, 'cart_count': cart_count})

def add_to_cart(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        cart = request.session.get('cart', {})
        cart[str(id)] = cart.get(str(id), 0) + 1
        request.session['cart'] = cart
        messages.success(request, f'¡"{product.name}" agregado al carrito exitosamente!')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

def subtract_from_cart(request, id):
    if request.method == 'POST':
        product_id = str(id)
        cart = request.session.get('cart', {})
        if product_id in cart:
            if cart[product_id] > 1:
                cart[product_id] -= 1
                messages.success(request, 'Cantidad disminuida.')
            else:
                del cart[product_id]
                messages.success(request, 'Producto eliminado del carrito.')
            request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'view_cart'))

def view_cart(request):
    cart = get_clean_cart(request)
    cart_items = []
    total_price = 0
    cart_count = sum(cart.values())
    
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total_price += subtotal
        
    return render(request, 'products/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    })

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Producto eliminado del carrito.')
    return redirect('view_cart')

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def load_dummy_data(request):
    if request.method == 'POST':
        cat_audio, _ = Category.objects.get_or_create(name="AUDIO")
        cat_perif, _ = Category.objects.get_or_create(name="PERIFÉRICOS")
        cat_moni, _ = Category.objects.get_or_create(name="MONITORES")
        cat_mueb, _ = Category.objects.get_or_create(name="MUEBLES")
        cat_acc, _ = Category.objects.get_or_create(name="ACCESORIOS")

        products_data = [
            {"name": "HEADSET HYPERION X", "cat": cat_audio, "price": 120000, "img": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=500&q=80"},
            {"name": "TECLADO MECÁNICO K-70", "cat": cat_perif, "price": 185000, "img": "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=500&q=80"},
            {"name": "MOUSE GAMER G-PRO", "cat": cat_perif, "price": 95000, "img": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?auto=format&fit=crop&w=500&q=80"},
            {"name": "MONITOR CURVO 144HZ", "cat": cat_moni, "price": 290000, "img": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80"},
            {"name": "SILLA GAMER OMEGA", "cat": cat_mueb, "price": 150000, "img": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?auto=format&fit=crop&w=500&q=80"},
            {"name": "MOUSEPAD RGB XXL", "cat": cat_acc, "price": 35000, "img": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=500&q=80"},
        ]

        dummy_names = [p["name"] for p in products_data]
        Product.objects.filter(name__in=dummy_names).delete()

        for p in products_data:
            Product.objects.create(
                name=p["name"],
                category=p["cat"], price=p["price"], stock=15, description="Producto autogenerado de muestra.", image_url=p["img"]
            )
        
        messages.success(request, '¡Catálogo de prueba restaurado y actualizado exitosamente!')
    return redirect('product_list')

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto forjado con éxito.')
            return redirect('product_list')
        else:
            messages.error(request, 'Error en la forja. Revisa los datos.')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Crear'})

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Editar'})

@login_required(login_url='/login/')
@user_passes_test(is_admin, login_url='/login/')
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto destruido.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido a Nexus Store, {user.username}!')
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'products/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Hola de nuevo, {user.username}!')
            return redirect('product_list')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('product_list')
