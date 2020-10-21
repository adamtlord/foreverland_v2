from django.contrib import admin

from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__email', 'user__first_name',
        'user__last_name')
    list_display = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)

# Hide uneeded stuff in admin.
from registration.models import RegistrationProfile
admin.site.unregister(RegistrationProfile)
