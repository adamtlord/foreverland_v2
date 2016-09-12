from django.contrib import admin
from shows.models import Venue, Show, Tour
from fidouche.models import Expense
from sorl.thumbnail.admin import AdminImageMixin


class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'city', 'state')
    search_fields = ['venue_name']

admin.site.register(Venue, VenueAdmin)


class ExpenseAdmin(AdminImageMixin, admin.ModelAdmin):
    pass

admin.site.register(Expense, ExpenseAdmin)


class ExpenseInline(admin.TabularInline):
    model = Expense


class ShowAdmin(admin.ModelAdmin):
    ordering = ['-date']
    inlines = [ExpenseInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "venue":
            kwargs["queryset"] = Venue.objects.order_by('venue_name')
        return super(ShowAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Show, ShowAdmin)

admin.site.register(Tour)
