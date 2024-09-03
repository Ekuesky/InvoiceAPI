from django import forms

from core_apps.customers.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [ "first_name",
                  "last_name",
                  "email",
                  "address",
                  "country",
                  "email", "phone_number",]