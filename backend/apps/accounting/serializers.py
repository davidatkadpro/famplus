from rest_framework import serializers

from .models import Account, Category, Journal, Transaction


class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Account
        fields = ["id", "name", "type", "balance"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ["id", "date", "memo"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "description",
            "amount",
            "debit_account",
            "credit_account",
            "category",
            "journal",
        ]
