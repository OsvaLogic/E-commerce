from django import forms
from .models import Product
from decimal import Decimal, InvalidOperation

class ProductForm(forms.ModelForm):
    # Sobrescribimos el campo price como CharField para manipular el texto antes de validarlo
    price = forms.CharField(label="Precio", widget=forms.TextInput(attrs={'class': 'val-input'}))

    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'image_url', 'description', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'val-input'}),
            'category': forms.Select(attrs={'class': 'val-input'}),
            'image': forms.FileInput(attrs={'class': 'val-input'}),
            'image_url': forms.URLInput(attrs={'class': 'val-input', 'placeholder': 'O pega un enlace de internet aquí...'}),
            'description': forms.Textarea(attrs={'class': 'val-input', 'rows': 3}),
            'stock': forms.NumberInput(attrs={'class': 'val-input'}),
        }

    def clean_price(self):
        price_data = self.cleaned_data.get('price')
        
        if isinstance(price_data, str):
            # Eliminamos los puntos (separador de miles chileno)
            price_data = price_data.replace('.', '')
            # Si por error pusieron coma en vez de punto para decimales, la reemplazamos
            price_data = price_data.replace(',', '.')
            
        try:
            price = Decimal(price_data)
        except InvalidOperation:
            raise forms.ValidationError("Ingrese un precio válido.")
            
        if price <= 0:
            raise forms.ValidationError("El precio debe ser superior a 0.")
        return price
