from django.urls import path
from .views import GeneratePDFInvoice, CreateInvoiceWithDetails, RetrieveInvoiceView

urlpatterns = [
    path("<uuid:invoice_id>/generate_pdf", GeneratePDFInvoice.as_view(), name="generate_pdf_invoice"),
    path("", CreateInvoiceWithDetails.as_view(), name="create_invoice"),
    path("<uuid:id>", RetrieveInvoiceView.as_view(), name="retrieve_invoice"),
]