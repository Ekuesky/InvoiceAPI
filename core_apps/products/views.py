# create views for category model and  product model
from rest_framework.exceptions import PermissionDenied

from .serializers import CategorySerializer, ProductSerializer, CreateProductSerializer
from rest_framework import permissions, generics
from.models import Category, Product
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # check if user is admin
        if not self.request.user.is_superuser:
            raise PermissionDenied(_('Only admin users can perform this action.'))

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProductSerializer
        return ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'
    def perform_destroy(self, instance):
        # check if user is admin or owner of product
        if not self.request.user.is_superuser :
            raise PermissionDenied(_('Only admin users or owner of the product can perform this action.'))

    # define a partial_update on price of the product
    def partial_update(self, request, *args, **kwargs):
        # update the product price
        partial_update_fields = request.data.keys()
        if 'price' in partial_update_fields:
            product = self.get_object()
            """
            if  not self.request.user.is_superuser:
                raise PermissionDenied(_('Only admin users or owner of the product can update its price.'))
            """
        return super().partial_update(request, *args, **kwargs)


