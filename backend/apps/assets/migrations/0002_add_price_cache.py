# Generated by Django 5.2 on 2025-07-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="current_price",
            field=models.DecimalField(
                blank=True, decimal_places=4, max_digits=12, null=True
            ),
        ),
        migrations.AddField(
            model_name="asset",
            name="price_fetched_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
