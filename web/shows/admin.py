from django.contrib import admin
from shows.models import Venue, Show, Tour
from fidouche.models import Expense
from sorl.thumbnail.admin import AdminImageMixin


class VenueAdmin(admin.ModelAdmin):
    list_display = ("venue_name", "city", "state")
    search_fields = ["venue_name"]


admin.site.register(Venue, VenueAdmin)


class ExpenseAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


admin.site.register(Expense, ExpenseAdmin)


class ExpenseInline(admin.TabularInline):
    model = Expense


class ShowAdmin(admin.ModelAdmin):
    ordering = ["-date"]
    inlines = [ExpenseInline]
    autocomplete_fields = ["venue"]


admin.site.register(Show, ShowAdmin)
admin.site.register(Tour)
