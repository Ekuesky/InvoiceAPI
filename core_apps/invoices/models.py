from django.db import models
from backend.core_apps.common.models import TimeStampedModel
from backend.core_apps.customers.models import Customer
from backend.core_apps.products.models import Product

class Invoice(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    reference = models.CharField(max_length=20, unique=True)

    @property
    def calculate_reference(self):
        return f"{self.date.year}-{self.date.month:02d}-{self.id:04d}"

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
# Create invoicedetail model with product,invoice  and quantity

class InvoiceDetail(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='details')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Invoice Detail'
        verbose_name_plural = 'Invoice Details'
        unique_together = (('product', 'invoice'))

