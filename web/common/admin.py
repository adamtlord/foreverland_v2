from django.contrib import admin


# Hide uneeded stuff in admin.
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
admin.site.unregister(Site)
admin.site.unregister(Group)
