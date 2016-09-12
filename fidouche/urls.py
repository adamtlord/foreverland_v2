from django.conf.urls import url
from fidouche.views import *

urlpatterns = [
    url(r'^$', financial_dashboard, {}, name='financial_dashboard'),

    url(r'^(?P<year>\d{4})/', gigs_by_year, {}, name='gigs_by_year'),
    url(r'^gigs/year-over-year', gigs_year_over_year, {}, name='gigs_year_over_year'),
    url(r'^gigs/(?P<gig_id>\d+)/$', gig_finances, {}, name='gig_finances'),
    url(r'^gigs/view/(?P<gig_id>\d+)/$', gig_finances_view, {}, name='gig_finances_view'),

    url(r'^tours/$', tour_list, {}, name='tour_list'),
    url(r'^tours/(?P<tour_id>\d+)/$', tour_detail, {}, name='tour_detail'),

    url(r'^expenses/year/(?P<year>\d{4})/', expenses_list, {}, name='expenses_list'),
    url(r'^expenses/$', all_expenses_list, {}, name='all_expenses_list'),
    url(r'^expenses/(?P<expense_id>\d+)/$', expense_details, {}, name='expense_details'),
    url(r'^expenses/create/$', expense_create, {}, name='expense_create'),
    url(r'^expenses/delete/(?P<expense_id>\d+)/$', expense_delete, {}, name='expense_delete'),

    url(r'^income/year/(?P<year>\d{4})/', income_list, {}, name='income_list'),
    url(r'^income/$', all_income_list, {}, name='all_income_list'),
    url(r'^income/(?P<income_id>\d+)/$', income_details, {}, name='income_details'),
    url(r'^income/create/$', income_create, {}, name='income_create'),
    url(r'^income/delete/(?P<income_id>\d+)/$', income_delete, {}, name='income_delete'),

    url(r'^reports/$', finance_reports, {}, name='finance_reports'),
    url(r'^tax-reports/$', tax_reports, {}, name='tax_reports'),
    url(r'^member-payments/(?P<member_id>\d+)$', member_payments, {}, name='member_payments'),
    url(r'^sub-payments/(?P<sub_id>\d+)$', sub_payments, {}, name='sub_payments'),
    url(r'^vendor-payments/(?P<vendor_id>\d+)$', vendor_payments, {}, name='vendor_payments'),
    url(r'^production-payments/(?P<company_id>\d+)$', production_payments, {}, name='production_payments'),

    url(r'^map/$', venue_map, {}, name='venue_map'),
    url(r'^map-data/$', venue_map_data, {}, name='venue_map_data'),
]
