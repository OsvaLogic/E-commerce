from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'image_url', 'description', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'val-input'}),
            'category': forms.Select(attrs={'class': 'val-input'}),
            'image': forms.FileInput(attrs={'class': 'val-input'}),
            'image_url': forms.URLInput(attrs={'class': 'val-input', 'placeholder': 'O pega un enlace de internet aquí...'}),
            'description': forms.Textarea(attrs={'class': 'val-input', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'val-input'}),
            'stock': forms.NumberInput(attrs={'class': 'val-input'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("El precio debe ser superior a 0.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if not image and not image_url:
            raise forms.ValidationError("Debes proporcionar una imagen (subiéndola o desde una URL).")
        
        if image and image_url:
            raise forms.ValidationError("No puedes proporcionar una imagen subida y una URL a la vez. Elige solo una.")
        
        return cleaned_data
