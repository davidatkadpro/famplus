import csv

from apps.families.mixins import FamilyQuerySetMixin
from django.http import StreamingHttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Account, Category, Journal, Transaction
from .serializers import (
    AccountSerializer,
    CategorySerializer,
    JournalSerializer,
    TransactionSerializer,
)


class AccountViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by("id")
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)


class CategoryViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)


class JournalViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = Journal.objects.all().order_by("-date")
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)


class TransactionViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("id")
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)

    @action(detail=False, methods=["post"])
    def import_csv(self, request):
        family = request.user.membership_set.first().family
        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response(
                {"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        decoded = uploaded.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded)
        created = 0
        for row in reader:
            Transaction.objects.create(
                family=family,
                description=row["description"],
                amount=row["amount"],
                debit_account_id=row["debit_account"],
                credit_account_id=row["credit_account"],
                category_id=row.get("category") or None,
                journal_id=row.get("journal") or None,
            )
            created += 1
        return Response({"created": created}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def export_csv(self, request):
        family = request.user.membership_set.first().family
        queryset = Transaction.objects.filter(family=family).order_by("id")

        headers = [
            "id",
            "description",
            "amount",
            "debit_account",
            "credit_account",
            "category",
            "journal",
        ]

        def generate():
            yield ",".join(headers) + "\n"
            for tx in queryset:
                row = [
                    str(tx.id),
                    tx.description,
                    str(tx.amount),
                    str(tx.debit_account_id),
                    str(tx.credit_account_id),
                    str(tx.category_id or ""),
                    str(tx.journal_id or ""),
                ]
                yield ",".join(row) + "\n"

        response = StreamingHttpResponse(generate(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=transactions.csv"
        return response
