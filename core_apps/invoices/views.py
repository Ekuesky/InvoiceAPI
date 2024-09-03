from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice
from .serializers import InvoiceSerializer, CreateInvoiceSerializer

from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML


def calculer_prix_ttc(prix_ht, tva, quantite):
    prix_ttc = (prix_ht * (1 + tva)) * quantite
    return prix_ttc

class GeneratePDFInvoice(APIView):
    def get(self, request, invoice_id):

        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice)
        template_path = 'invoice_template.html'
        context = {'invoice': serializer.data}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="invoice_{invoice.reference}.pdf"'

        # Rendu du template HTML
        html_template = get_template(template_path)
        html = html_template.render(context)

        # Génération du PDF avec WeasyPrint
        HTML(string=html).write_pdf(response)

        return response
class CreateInvoiceWithDetails(APIView):
    def post(self, request):
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveInvoiceView(RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]  # Add authentication if needed
    lookup_field = 'id'
