from rest_framework import serializers

from .models import Chore, Entry


class ChoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chore
        fields = ["id", "name", "schedule", "points", "archived"]


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = [
            "id",
            "chore",
            "assigned_to",
            "due_date",
            "status",
        ]
