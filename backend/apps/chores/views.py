from apps.accounting.models import Account
from apps.families.mixins import FamilyQuerySetMixin
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chore, Entry
from .serializers import ChoreSerializer, EntrySerializer
from .services import exchange_points


class ChoreViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = Chore.objects.all().order_by("id")
    serializer_class = ChoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)


class EntryViewSet(FamilyQuerySetMixin, viewsets.ModelViewSet):
    queryset = Entry.objects.all().order_by("-due_date")
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.membership_set.first().family)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        entry = self.get_object()
        entry.status = Entry.Status.APPROVED
        entry.save(update_fields=["status"])
        return Response({"status": entry.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Reject a completed entry."""
        entry = self.get_object()
        entry.status = Entry.Status.REJECTED
        entry.save(update_fields=["status"])
        return Response({"status": entry.status}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def exchange_points(self, request):
        account_id = request.data.get("account")
        points = int(request.data.get("points", 0))
        if not account_id or points <= 0:
            return Response(
                {"detail": "account and positive points required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        family = request.user.membership_set.first().family
        account = Account.objects.get(id=account_id, family=family)
        try:
            tx = exchange_points(request.user, account, points)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"transaction": tx.id}, status=status.HTTP_201_CREATED)
