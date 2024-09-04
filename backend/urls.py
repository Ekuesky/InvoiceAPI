
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from core_apps.users.views import CustomUserDetailsView
from dj_rest_auth.registration.views import RegisterView
from core_apps.users.views import CustomRegisterView

#web
from core_apps.invoices.web.views import Create_invoice, Invoice_detail
from core_apps.customers.web.views import Create_customer, Customer_list
from core_apps.products.web.views import Add_product, Product_list, Product_edit

schema_view = get_schema_view(
    openapi.Info(
        title="Invoice ",
        default_version="v1",
        description="new invoice",
        contact=openapi.Contact(email="ayiekue9127@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # api routes
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/user/", CustomUserDetailsView.as_view(), name="user_details"),
    path("api/v1/auth/login/", LoginView.as_view(), name="rest_login"),
    path("api/v1/auth/logout/", LogoutView.as_view(), name="rest_logout"),
    path("api/v1/auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("api/v1/auth/registration/", CustomRegisterView.as_view(), name="rest_auth_registration"),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/v1/customers/", include("core_apps.customers.urls")),
    path("api/v1/products/", include("core_apps.products.urls")),
    path("api/v1/invoices/", include("core_apps.invoices.urls")),

    # web routes
    path('web/invoices/', Create_invoice, name='create_invoice'),
    path('web/invoices/<int:pk>/', Invoice_detail, name='invoice_detail'),
    path('web/customers/', Customer_list, name='customer_list'),
    path('web/customers/create', Create_customer, name='create_customer'),
    path('web/products/', Product_list, name='product_list'),
    path('web/products/add/', Add_product, name='product_add'),
    path('web/products/<uuid:product_id>/edit/', Product_edit, name='product_edit'),
]

admin.site.site_header = "Administration"

admin.site.site_title = "Invoice api"

admin.site.index_title = "Welcome to Invoice portal"
