# Generated by Django 4.2.15 on 2024-09-02 09:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_alter_product_tva"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="tva",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=4,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1),
                ],
            ),
        ),
    ]