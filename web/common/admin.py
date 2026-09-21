from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

# Hide unused built-in admin models.
admin.site.unregister(Site)
admin.site.unregister(Group)

SSN_VIEW_GROUP = "can_view_ssn"


def mask_ssn(value):
    if not value:
        return ""
    digits = "".join(c for c in str(value) if c.isdigit())
    last4 = digits[-4:] if len(digits) >= 4 else "••••"
    return "•••-••-%s" % last4


def can_view_ssn(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=SSN_VIEW_GROUP).exists()


class MaskedSSNAdmin(admin.ModelAdmin):
    """Hide raw SSNs unless the user is a superuser or in can_view_ssn."""

    def get_exclude(self, request, obj=None):
        exclude = list(super().get_exclude(request, obj) or [])
        if not can_view_ssn(request.user) and "ssn" not in exclude:
            exclude.append("ssn")
        return exclude

    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if not can_view_ssn(request.user) and "ssn_masked" not in ro:
            ro.append("ssn_masked")
        return ro

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if fields is None:
            return fields
        fields = list(fields)
        if not can_view_ssn(request.user):
            fields = ["ssn_masked" if f == "ssn" else f for f in fields]
            if "ssn" in fields:
                fields.remove("ssn")
            if "ssn_masked" not in fields:
                fields.append("ssn_masked")
        return fields

    def ssn_masked(self, obj):
        return mask_ssn(getattr(obj, "ssn", "") if obj else "")

    ssn_masked.short_description = "SSN#"
