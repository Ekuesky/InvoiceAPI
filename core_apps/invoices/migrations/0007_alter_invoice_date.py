# Generated by Django 5.1 on 2024-08-30 19:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("invoices", "0006_alter_invoice_reference"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
