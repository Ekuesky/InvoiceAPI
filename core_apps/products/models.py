from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from core_apps.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _



# create a Category model with label
class Category(TimeStampedModel):
    label = models.CharField(max_length=200, unique=True)

# create a product model with label, brand, reference, category, description, price, tva
class Product(TimeStampedModel):
    label = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    reference = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")
    description = models.TextField( verbose_name=_("product description"),)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #make max value of tva to 1 and min to 0
    tva = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")




