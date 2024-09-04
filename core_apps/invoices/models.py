from datetime import date

from django.utils import timezone
import hashlib

from django.db import models
from core_apps.common.models import TimeStampedModel
from core_apps.customers.models import Customer
from core_apps.products.models import Product

class Invoice(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    # set default date to now
    date = models.DateField(auto_now_add=True,)
    reference = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.date:
            current_date = date.today()
            self.date = current_date

        # if not self.reference:
        #     hash_input = f"{self.date.month}-{self.date.day}"
        #     reference_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        #     self.reference = reference_hash[:8].upper()+'-'+str(self.pk)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

class InvoiceDetail(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='details')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Invoice Detail'
        verbose_name_plural = 'Invoice Details'
        unique_together = ('invoice', 'product')

