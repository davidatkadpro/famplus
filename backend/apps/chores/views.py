from rest_framework import permissions, viewsets

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
