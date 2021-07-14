from django.contrib import admin
from django.contrib.auth.models import Group
# Hide uneeded stuff in admin.
from django.contrib.sites.models import Site

admin.site.unregister(Site)
admin.site.unregister(Group)
