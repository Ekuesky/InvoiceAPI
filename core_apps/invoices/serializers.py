from rest_framework import serializers
from .models import Invoice, InvoiceDetail
from core_apps.customers.serializers import CustomerSerializer
from core_apps.products.serializers import ProductSerializer
from django.db import transaction

from ..customers.models import Customer
from ..products.models import Product


class InvoiceDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = InvoiceDetail
        fields = ['product', 'quantity']


class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    details = InvoiceDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'amount', 'date', 'reference', 'details']
        read_only_fields = ['date', 'reference', 'amount']


class InvoiceDetailCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField()

    class Meta:
        model = InvoiceDetail
        fields = ['product_id', 'quantity']



class CreateInvoiceSerializer(serializers.ModelSerializer):
    customer_id = serializers.UUIDField()
    details = InvoiceDetailCreateSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id','customer_id', 'date', 'details', 'reference', 'amount']
        read_only_fields = ['reference', 'amount']

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        details_data = validated_data.pop('details')

        try:
            customer = Customer.objects.get(id=customer_id)

        except Customer.DoesNotExist:
            raise serializers.ValidationError({'customer_id': 'Customer not found'})

        invoice = Invoice.objects.create(customer=customer, **validated_data)  # Create outside the transaction

        try:
            with transaction.atomic():  # Transaction for InvoiceDetail only
                # Accumuler les quantités pour les produits en double
                product_quantities = {}
                for detail_data in details_data:
                    product_id = detail_data.pop('product_id')
                    try:
                        product = Product.objects.get(id=product_id)
                    except Product.DoesNotExist:
                        raise serializers.ValidationError({'product_id': f'Product with ID {product_id} not found'})

                    if product_id in product_quantities:
                        product_quantities[product_id] += detail_data['quantity']
                    else:
                        product_quantities[product_id] = detail_data['quantity']

                # Créer les InvoiceDetail avec les quantités accumulées

                for product_id, quantity in product_quantities.items():
                    product = Product.objects.get(id=product_id)
                    InvoiceDetail.objects.create(invoice=invoice, product=product, quantity=quantity)

                invoice.amount = 0
                for detail in invoice.details.all():
                    invoice.amount += detail.product.price * (1+detail.product.tva)* detail.quantity
                invoice.save()

                invoice_data = super().to_representation(invoice)
                invoice_data['id'] = invoice.id
                invoice_data['customer_id'] = customer_id
                return invoice_data


        except Exception as e:
            invoice.delete()  # Delete invoice if InvoiceDetail creation fails
            raise serializers.ValidationError({'error': f'An error occurred: {str(e)}'})  # Re-raise the error
