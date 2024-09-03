from django.db import models
from core_apps.common.models import TimeStampedModel
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class Customer(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.TextField()
    postal_code = models.CharField(max_length=100)
    country = CountryField(
        verbose_name=_("country"), default=_("TG"), blank=False, null=False
    )
    email = models.EmailField(db_index=True, unique=True)
    phone_number = PhoneNumberField(verbose_name=_(" first phone number"), max_length=30, default="+22891271298" )
    phone_number2 = PhoneNumberField(verbose_name=_(" second phone number"), max_length=30, null=True )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Customers"

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return f"{self.first_name.title()}"