from accounts.models import UserProfile
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    list_display = ("user",)


admin.site.register(UserProfile, UserProfileAdmin)
