from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Invoice, InvoiceDetail
from core_apps.invoices.web.forms import InvoiceForm, InvoiceDetailForm
from ...customers.models import Customer
from ...products.models import Product, Category

def calculer_prix_ttc(prix_ht, tva, quantite):
    prix_ttc = (prix_ht * (1 + tva)) * quantite
    return prix_ttc

@login_required
def Create_invoice(request):
  if request.method == 'POST':
    invoice_form = InvoiceForm(request.POST)
    if invoice_form.is_valid():
      invoice = invoice_form.save()

      total_amount = 0
      i = 1
      while True:
        product_id = request.POST.get(f'product-{i}-id')
        quantity = request.POST.get(f'quantity-{i}')

        if product_id is None or quantity is None:
          break

        product = Product.objects.get(id=product_id)
        InvoiceDetail.objects.create(invoice=invoice, product=product, quantity=quantity)

        # Calcul du prix TTC pour chaque produit
        prix_ttc = calculer_prix_ttc(product.price, product.tva, int(quantity))
        # Ajout au montant total
        total_amount += prix_ttc

        i += 1
        # Mise à jour du montant total de la facture
      invoice.amount = total_amount
      invoice.save()

      return redirect('invoice_detail', pk=invoice.pk)
    else:
      print(invoice_form.errors)
  else:
    invoice_form = InvoiceForm()

  customers = Customer.objects.all()
  products = Product.objects.all()
  categories = Category.objects.all()
  context = {'customers': customers, 'products': products, 'categories': categories,  'invoice_form': invoice_form}
  return render(request, 'create_invoice.html', context)

def Invoice_detail(request, pk):
    lookup_field = 'id'
    invoice = get_object_or_404(Invoice, pk=pk)
    context = {'invoice': invoice}
    return render(request, 'invoice_detail.html', context)