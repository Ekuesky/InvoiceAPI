from django.http import Http404
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import CustomerSerializer
from.models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            raise NotFound(
                {
                    "detail": "Le client n'existe pas",
                    "code": "client_not_found",
                }
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

