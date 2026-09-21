from common.admin import MaskedSSNAdmin
from django.contrib import admin
from members.models import Member, Sub


class MemberAdmin(MaskedSSNAdmin):
    pass


admin.site.register(Member, MemberAdmin)


class SubAdmin(MaskedSSNAdmin):
    pass


admin.site.register(Sub, SubAdmin)
