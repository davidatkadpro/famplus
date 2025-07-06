from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    @action(detail=False, methods=["post"])
    def mark_read(self, request):
        ids = request.data.get("ids", [])
        updated = Notification.objects.filter(user=request.user, id__in=ids).update(
            read=True
        )
        return Response({"marked": updated}, status=status.HTTP_200_OK)
