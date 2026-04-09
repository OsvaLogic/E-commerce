from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    # Configura las columnas para tener una vista previa rápida en el panel
    list_display = ('id', 'name', 'price', 'stock')
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)