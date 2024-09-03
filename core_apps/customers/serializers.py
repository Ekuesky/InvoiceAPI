from rest_framework import serializers
from .models import Customer
from django_countries.serializer_fields import CountryField

class CustomerSerializer(serializers.ModelSerializer):

    country = CountryField(name_only=True)

    class Meta:
        model = Customer
        fields = ['id',
                  "first_name",
                  "last_name",
                  "email",
                  "address",
                  "country",
                  "email", "phone_number", "created_at","updated_at"]



