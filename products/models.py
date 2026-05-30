from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre de la Categoría")

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    description = models.TextField(verbose_name="Descripción")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL de la Imagen")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Subir Imagen")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self):
        return self.name


class Factura(models.Model):
    # max_digits=8 permite hasta 999.999
    monto = models.DecimalField(max_digits=10, decimal_places=0)

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('PAID', 'Pagado'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregado'),
        ('CANCELED', 'Cancelado'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado")
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Total")

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # SET_NULL por si el producto es eliminado del catálogo a futuro
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Producto Eliminado'}"
