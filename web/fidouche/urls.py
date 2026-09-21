from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from fidouche.views import (all_expenses_list, all_income_list, expense_create,
                            expense_delete, expense_details, expenses_list,
                            finance_reports, financial_dashboard, gig_finances,
                            gig_finances_view, gigs_by_year,
                            gigs_year_over_year, income_create, income_delete,
                            income_details, income_list, member_payments,
                            private_receipt, production_payments, sub_payments,
                            tax_reports, tour_detail, tour_list,
                            vendor_payments, venue_map, venue_map_data)

# Every fidouche URL is finance data. Writes were already staff-gated; reads were not.
def staff(view):
    return staff_member_required(view)


urlpatterns = [
    path("", staff(financial_dashboard), {}, name="financial_dashboard"),
    path("<int:year>/", staff(gigs_by_year), {}, name="gigs_by_year"),
    path(
        "gigs/year-over-year",
        staff(gigs_year_over_year),
        {},
        name="gigs_year_over_year",
    ),
    path("gigs/<int:gig_id>/", staff(gig_finances), {}, name="gig_finances"),
    path(
        "gigs/view/<int:gig_id>/",
        staff(gig_finances_view),
        {},
        name="gig_finances_view",
    ),
    path("tours/", staff(tour_list), {}, name="tour_list"),
    path("tours/<int:tour_id>/", staff(tour_detail), {}, name="tour_detail"),
    path("expenses/year/<int:year>/", staff(expenses_list), {}, name="expenses_list"),
    path("expenses/", staff(all_expenses_list), {}, name="all_expenses_list"),
    path("expenses/<int:expense_id>/", staff(expense_details), {}, name="expense_details"),
    path("expenses/create/", staff(expense_create), {}, name="expense_create"),
    path(
        "expenses/delete/<int:expense_id>/",
        staff(expense_delete),
        {},
        name="expense_delete",
    ),
    path("income/year/<int:year>/", staff(income_list), {}, name="income_list"),
    path("income/", staff(all_income_list), {}, name="all_income_list"),
    path("income/<int:income_id>/", staff(income_details), {}, name="income_details"),
    path("income/create/", staff(income_create), {}, name="income_create"),
    path("income/delete/<int:income_id>/", staff(income_delete), {}, name="income_delete"),
    path("reports/", staff(finance_reports), {}, name="finance_reports"),
    path("tax-reports/", staff(tax_reports), {}, name="tax_reports"),
    path(
        "member-payments/<int:member_id>/",
        staff(member_payments),
        {},
        name="member_payments",
    ),
    path("sub-payments/<int:sub_id>/", staff(sub_payments), {}, name="sub_payments"),
    path(
        "vendor-payments/<int:vendor_id>/",
        staff(vendor_payments),
        {},
        name="vendor_payments",
    ),
    path(
        "production-payments/<int:company_id>/",
        staff(production_payments),
        {},
        name="production_payments",
    ),
    path("map/", staff(venue_map), {}, name="venue_map"),
    path("map-data/", staff(venue_map_data), {}, name="venue_map_data"),
    path(
        "receipts/<path:filename>",
        staff(private_receipt),
        name="private_receipt",
    ),
]
