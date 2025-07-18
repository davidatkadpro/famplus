# Generated by Django 5.2 on 2025-07-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0001_initial"),
        ("assets", "0002_add_price_cache"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="assets",
            field=models.ManyToManyField(
                blank=True, related_name="accounts", to="assets.asset"
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="interest_rate",
            field=models.DecimalField(
                decimal_places=4,
                default=0,
                help_text="Monthly interest rate as decimal (e.g. 0.01 for 1%)",
                max_digits=5,
            ),
        ),
    ]
