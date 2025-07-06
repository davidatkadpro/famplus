from django.contrib import admin

from .models import Family, Invitation, Membership


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "family", "role")
    list_filter = ("role",)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "family", "role", "accepted")
    list_filter = ("role", "accepted")
