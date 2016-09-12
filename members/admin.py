from django.contrib import admin
from members.models import Member, Sub


class MemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Member, MemberAdmin)


class SubAdmin(admin.ModelAdmin):
	pass

admin.site.register(Sub, SubAdmin)
