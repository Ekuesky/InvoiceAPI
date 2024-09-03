from django import forms
from core_apps.invoices.models import Invoice, InvoiceDetail
from core_apps.customers.models import Customer
from core_apps.products.models import Product


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all()

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()