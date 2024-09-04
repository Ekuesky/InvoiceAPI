from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Product, Category
from .forms import ProductForm
from django.contrib import messages
from django.db import IntegrityError  # Import IntegrityError

def Product_list(request):
  products = Product.objects.all()
  categories = Category.objects.all()
  paginator = Paginator(products, 10)  # 10 products per page
  page_number = request.GET.get('page')
  products = paginator.get_page(page_number)
  return render(request, 'product_list.html', {'products': products, 'categories': categories})


def Add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                category_id = request.POST.get('category')
                #convert price and tva to decimal from request.POST
                product.price = float(request.POST.get('price'))
                product.tva = float(request.POST.get('tva'))

                category = Category.objects.get(pkid=category_id)
                product.category = category
                product.save()
                return redirect('product_list')
            except IntegrityError:
                messages.error(request, 'A product with these details already exists.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
    else:
        form = ProductForm()

    return render(request, 'add.html', {'form': form, 'categories': categories})


def Product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()  # Get all categories for the dropdown

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès !')
            return redirect('product_list')  # Replace with the URL name of your product list view
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_edit.html', {'form': form, 'product': product, 'categories': categories})