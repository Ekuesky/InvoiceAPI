from django import forms
from ..models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'label', 'brand', 'price', 'reference', 'description', 'tva', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-select'}), # For Bootstrap styling
        }
    def clean_tva(self):
        tva = self.cleaned_data['tva']
        if tva < 0 or tva > 1:
            raise forms.ValidationError("TVA must be between 0 and 1.")
        return tva