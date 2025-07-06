from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chore, Entry
from .serializers import ChoreSerializer, EntrySerializer


class ChoreViewSet(viewsets.ModelViewSet):
    queryset = Chore.objects.all().order_by("id")
    serializer_class = ChoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all().order_by("-due_date")
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.memberships.first().family)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        entry = self.get_object()
        entry.status = Entry.Status.APPROVED
        entry.save(update_fields=["status"])
        return Response({"status": entry.status}, status=status.HTTP_200_OK)
