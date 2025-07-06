from rest_framework import permissions, viewsets

from .models import Account, Category, Journal, Transaction
from .serializers import (
    AccountSerializer,
    CategorySerializer,
    JournalSerializer,
    TransactionSerializer,
)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by("id")
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all().order_by("-date")
    serializer_class = JournalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("id")
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)
