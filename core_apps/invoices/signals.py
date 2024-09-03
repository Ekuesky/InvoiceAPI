from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InvoiceDetail

@receiver(post_save, sender=InvoiceDetail)
def update_invoice_amount(sender, instance, created, **kwargs):
    if created or instance.quantity_changed:
        invoice = instance.invoice
        invoice.save()