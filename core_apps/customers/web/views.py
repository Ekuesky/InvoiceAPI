from django.shortcuts import render, redirect

from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django_countries import countries
from django.contrib import messages

from core_apps.customers.models import Customer


@login_required
def Customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers, 'countries': countries})

@login_required
def Create_customer(request):
    if request.method == 'POST':
        # Récupérez les données du formulaire
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        country = request.POST['country']
        phone_number = request.POST['phone_number']

        # Récupérez l'utilisateur connecté
        user = request.user

        try:
            # Créez un nouvel objet Customer
            customer = Customer(
                user=user,  # Associez l'utilisateur au client
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                country=country,
                phone_number=phone_number,
            )
            customer.save()

            # Redirigez vers la liste des clients
            return redirect('customer_list')

        except IntegrityError:
            # Un email unique existe déjà, afficher un message d'erreur
            messages.error(request, 'This email address is already in use.')

    # Si le formulaire n'est pas soumis ou s'il y a une erreur, afficher le formulaire
    return render(request, 'customer_list.html', {'countries': countries})