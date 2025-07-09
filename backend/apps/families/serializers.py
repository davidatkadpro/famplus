"""Serializers for families app."""

from rest_framework import serializers

from .models import Family, Membership, Invitation


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["id", "name", "settings_json"]


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["id", "user", "family", "role"]


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["id", "email", "family", "role", "code", "accepted", "created"]
        read_only_fields = ["code", "accepted", "created"]
