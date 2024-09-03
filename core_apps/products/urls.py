from .views import  ProductListCreateView,ProductDetailView, CategoryDetailView, CategoryListCreateView
from django.urls import path

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:id>/', CategoryDetailView.as_view(), name='category-detail'),
]