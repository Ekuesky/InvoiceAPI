from django.urls import path

from .views import CustomerListCreateView, CustomerDetailView

urlpatterns = [
    path("", CustomerListCreateView.as_view(), name="client-list-create"),
    path(
        "<uuid:id>/",
        CustomerDetailView.as_view(),
        name="client-retrieve-update-destroy",
    ),
]
