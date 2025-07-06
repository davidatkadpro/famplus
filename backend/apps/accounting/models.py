from apps.families.models import FamilyScopedModel
from django.db import models


class Account(FamilyScopedModel):
    class Type(models.TextChoices):
        ASSET = "asset", "Asset"
        LIABILITY = "liability", "Liability"
        EQUITY = "equity", "Equity"
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type.choices)
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0,
        help_text="Monthly interest rate as decimal (e.g. 0.01 for 1%)",
    )
    assets = models.ManyToManyField("assets.Asset", blank=True, related_name="accounts")

    @property
    def balance(self):
        """Current balance computed from related transactions."""
        from django.db.models import Sum
        from django.db.models.functions import Coalesce

        debit_sum = self.debits.aggregate(
            total=Coalesce(
                Sum("amount"),
                0,
                output_field=models.DecimalField(max_digits=10, decimal_places=2),
            )
        )["total"]
        credit_sum = self.credits.aggregate(
            total=Coalesce(
                Sum("amount"),
                0,
                output_field=models.DecimalField(max_digits=10, decimal_places=2),
            )
        )["total"]
        return debit_sum - credit_sum

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.name


class Category(FamilyScopedModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.name


class Journal(FamilyScopedModel):
    date = models.DateField()
    memo = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"Journal {self.date}"  # type: ignore[str-format]


class Transaction(FamilyScopedModel):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    debit_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="debits"
    )
    credit_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="credits"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    journal = models.ForeignKey(
        Journal, on_delete=models.SET_NULL, null=True, blank=True
    )

    def clean(self):
        super().clean()
        from django.core.exceptions import ValidationError

        if self.debit_account_id == self.credit_account_id:
            raise ValidationError("Debit and credit accounts cannot be the same.")
        if self.amount <= 0:
            raise ValidationError("Transaction amount must be positive.")

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.description

    def save(self, *args, **kwargs):
        # Ensure accounts belong to same family
        if self.debit_account.family_id != self.family_id:
            self.family = self.debit_account.family
        self.full_clean()
        super().save(*args, **kwargs)
