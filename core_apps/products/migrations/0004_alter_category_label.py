# Generated by Django 4.2.15 on 2024-09-02 17:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_product_tva"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="label",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]