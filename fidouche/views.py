from datetime import date
from time import strftime
import random
import datetime
import json
from itertools import chain
from collections import defaultdict
from django.forms.models import inlineformset_factory
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from django.conf import settings

from members.models import Member, Sub
from shows.models import Show, Tour, Venue
from fidouche.models import Payment, SubPayment, Expense, TourExpense, Quote, CommissionPayment, \
    ProductionPayment, ProductionCategory, Payee, ProductionCompany, Income
from fidouche.forms import GigFinanceForm, ExpenseForm, TourExpenseForm, PaymentForm, SubPaymentForm, \
    ProductionPaymentForm, IncomeForm

current_year = date.today().year


@login_required
def financial_dashboard(request, template='fidouche/dashboard.html'):
    """"""
    gigs = Show.objects.filter(date__year=current_year)
    last_show = Show.objects.filter(date__lte=datetime.datetime.now()).order_by('-date')[0]
    next_show = gigs.filter(date__gte=datetime.datetime.now()).order_by('date')[0]
    gigs_booked = gigs.filter(date__year=current_year)
    gigs_played = gigs_booked.filter(date__lt=datetime.datetime.now())

    quotecount = Quote.objects.all().count()
    rslice = random.random() * (quotecount - 1)
    quotes = Quote.objects.all()[rslice: rslice+1]

    ytd_gross = []
    ytd_net = []
    ytd_player = []

    for gig in gigs:
        gig.production_costs = gig.get_production_costs()
        gig.expenses = gig.get_expenses()
        gig.total_expenses = gig.get_total_costs()

    for gig in gigs_played:
        if gig.gross:
            ytd_gross.append(gig.gross)
        if gig.net:
            ytd_net.append(gig.net)
        if gig.payout:
            ytd_player.append(gig.payout)

    ytd = {
        'gigs_booked': gigs_booked.count(),
        'gigs_played': gigs_played.count(),
        'net':  sum(ytd_net),
        'gross': sum(ytd_gross),
        'payout': sum(ytd_player)
    }

    d = {
        'gigs': gigs,
        'last_show': last_show,
        'next_show': next_show,
        'ytd': ytd,
        'quote': quotes[0]
    }
    return render(request, template, d)


@login_required
def gigs_by_year(request, year=current_year, template='fidouche/gigs_by_year.html'):
    """Listing of all gigs in the given year"""

    gigs = Show.objects.filter(date__year=year)
    current = False
    if int(year) == int(current_year):
        gigs = gigs.filter(date__lt=datetime.datetime.now())
        current = True
    by_month = {}
    players = []
    commission = []
    to_account = []
    gross = []
    net = []
    payout = []
    sum_all_expenses = []
    all_total_expenses = []

    for m in range(1, 13):
        month_gigs = gigs.filter(date__month=m)
        by_month[m] = {
            'count': month_gigs.count(),
            'gross': month_gigs.aggregate(Sum('gross'))
        }

    for gig in gigs:
        gig.production_costs = gig.get_production_costs()
        gig.expenses = gig.get_expenses()
        gig.tour_costs = gig.get_tour_costs()
        gig.total_expenses = gig.get_total_costs()
        all_total_expenses.append(gig.total_expenses)
        gig.payments = Payment.objects.filter(show=gig)
        if gig.payments:
            for pay in gig.payments:
                if pay.amount:
                    players.append(pay.amount)
        else:
            if gig.payout:
                players.append(gig.payout * 14)

        if gig.commission:
            commission.append(gig.commission)
        if gig.to_account:
            to_account.append(gig.to_account)
        if gig.gross:
            gross.append(gig.gross)
        if gig.net:
            net.append(gig.net)
        if gig.payout:
            payout.append(gig.payout)
        gig.all_expenses = dict(gig.production_costs.items() + gig.expenses.items() + gig.tour_costs.items())
        sum_all_expenses.append(gig.all_expenses)

    # http://stackoverflow.com/questions/19461747/sum-corresponding-elements-of-multiple-python-dictionaries
    from collections import Counter
    summed_expenses = Counter()
    for d in sum_all_expenses:
        summed_expenses.update(d)

    d = {
        'year': year,
        'this_years_gigs': gigs,
        'gigs_played': gigs.count(),
        'gross': sum(gross),
        'net': sum(net),
        'payout': sum(payout),
        'current': current,
        'by_month': by_month,
        'players': sum(players),
        'commission': sum(commission),
        'all_expenses': dict(summed_expenses),
        'total_expenses': sum(all_total_expenses),
        'to_account': sum(to_account)
    }
    return render(request, template, d)


@login_required
def gigs_year_over_year(request, template='fidouche/gigs_year_over_year.html'):
    d = {}
    from common.utils import years_with_gigs
    years_with_gigs = years_with_gigs()
    gigs = Show.objects.all()
    years = {}
    players = []
    commission = []
    sum_all_expenses = []
    all_total_expenses = []
    for year in years_with_gigs:
        years[year] = {}
        this_years_gigs = gigs.filter(date__year=year)
        y_gross = []
        y_net = []
        y_player = []
        for gig in this_years_gigs:
            if gig.gross:
                y_gross.append(gig.gross)
            if gig.net:
                y_net.append(gig.net)
            if gig.payout:
                y_player.append(gig.payout)
        years[year] = {
            'gigs_played': this_years_gigs.count(),
            'net':  sum(y_net),
            'gross': sum(y_gross),
            'payout': sum(y_player)
        }
    d['years'] = years

    for gig in gigs:
        gig.production_costs = gig.get_production_costs()
        gig.expenses = gig.get_expenses()
        gig.tour_costs = gig.get_tour_costs()
        gig.total_expenses = gig.get_total_costs()
        all_total_expenses.append(gig.total_expenses)
        gig.payments = Payment.objects.filter(show=gig)
        if gig.payments:
            for pay in gig.payments:
                if pay.amount:
                    players.append(pay.amount)
        else:
            if gig.payout:
                players.append(gig.payout * 14)
        if gig.commission:
            commission.append(gig.commission)
        gig.all_expenses = dict(gig.production_costs.items() + gig.expenses.items() + gig.tour_costs.items())
        sum_all_expenses.append(gig.all_expenses)

    d['all_gigs'] = gigs
    return render(request, template, d)


@login_required
@staff_member_required
def gig_finances(request, gig_id=None, template='fidouche/gig_finances.html'):
    """Choose a gig from this year"""

    gig_id = int(gig_id)
    gig = get_object_or_404(Show, pk=gig_id)
    active_members = Member.objects.filter(active=True)
    iem_cat = ProductionCategory.objects.filter(name__icontains="iem")[0]

    members_to_pay = [member for member in active_members]

    ExpenseFormSet = inlineformset_factory(Show, Expense, form=ExpenseForm)
    PaymentFormSet = inlineformset_factory(Show, Payment, form=PaymentForm, extra=len(active_members), max_num=14)
    SubPaymentFormSet = inlineformset_factory(Show, SubPayment, form=SubPaymentForm, extra=1)
    ProductionPaymentFormSet = inlineformset_factory(Show, ProductionPayment, extra=1, form=ProductionPaymentForm)

    if request.method == "POST":

        form = GigFinanceForm(request.POST, request.FILES, instance=gig)
        expense_formset = ExpenseFormSet(request.POST, request.FILES, instance=gig)
        payment_formset = PaymentFormSet(request.POST, instance=gig)
        sub_payment_formset = SubPaymentFormSet(request.POST, instance=gig)
        production_payment_formset = ProductionPaymentFormSet(request.POST, instance=gig)
        if form.is_valid() and \
           expense_formset.is_valid() and \
           payment_formset.is_valid() and \
           sub_payment_formset.is_valid() and \
           production_payment_formset.is_valid():
                form.save()
                expense_formset.save()
                payment_formset.save()
                sub_payment_formset.save()
                production_payment_formset.save()

                cdata = form.cleaned_data
                if not cdata['commission_withheld']:
                    commission_payment, created = CommissionPayment.objects.get_or_create(show=gig)
                    commission_payment.agent = cdata['agent']
                    commission_payment.amount = cdata['commission']
                    commission_payment.paid = cdata['commission_paid']
                    commission_payment.check_no = cdata['commission_check_no']
                    commission_payment.save()

                messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>NICE.</strong> Gig finances updated!')
                return redirect(request.path)
        else:
            messages.add_message(request, messages.ERROR, '<i class="fa fa-wrench"></i> <strong>Aw, damnit.</strong> Something\'s fucked up.')
    else:
        initial_data = {}
        if not gig.agent:
            initial_data['agent'] = 1

        form = GigFinanceForm(instance=gig, initial=initial_data)
        expense_formset = ExpenseFormSet(instance=gig)
        payment_formset = PaymentFormSet(instance=gig)
        sub_payment_formset = SubPaymentFormSet(instance=gig)
        production_payment_formset = ProductionPaymentFormSet(instance=gig)

        if all(v is None for v in [sf['member'].value() for sf in payment_formset.forms]):
            for subform, data in zip(payment_formset.forms, members_to_pay):
                subform.initial['member'] = data

    next_shows = Show.objects.filter(date__gt=gig.date).order_by('date')
    if next_shows:
        next_show = next_shows[0]
    else:
        next_show = None

    d = {
        'form': form,
        'expense_formset': expense_formset,
        'payment_formset': payment_formset,
        'sub_payment_formset': sub_payment_formset,
        'production_payment_formset': production_payment_formset,
        'gig': gig,
        'iem_cat': iem_cat.id,
        'next_show': next_show
    }

    return render(request, template, d)


@login_required
def gig_finances_view(request, gig_id=None, template='fidouche/gig_finances_view.html'):
    """Read-only view of gig finance info"""

    gig_id = int(gig_id)
    gig = get_object_or_404(Show, pk=gig_id)
    payments = Payment.objects.filter(show=gig)
    sub_payments = SubPayment.objects.filter(show=gig)
    expenses = Expense.objects.filter(show=gig)
    buyouts = False
    if gig.fee or gig.food_buyout or gig.travel_buyout or gig.lodging_buyout or gig.other_buyout:
        buyouts = True

    d = {
        'gig': gig,
        'payments': payments,
        'sub_payments': sub_payments,
        'expenses': expenses,
        'buyouts': buyouts
    }

    return render(request, template, d)


@login_required
def expenses_list(request, year=current_year, template='fidouche/expenses_list.html'):
    """Show non-gig expenses"""
    expenses = Expense.objects.filter(show__isnull=True, date__year=year)
    # tour_expenses = TourExpense.objects.filter(date__year=year)
    # all_expenses = list(chain(expenses, tour_expenses))
    d = {
        'expenses': expenses
    }

    return render(request, template, d)


@login_required
def all_expenses_list(request, template='fidouche/expenses_list.html'):
    """Show non-gig expenses"""
    expenses = Expense.objects.filter(show__isnull=True)
    tour_expenses = TourExpense.objects.all()
    all_expenses = list(chain(expenses, tour_expenses))
    d = {
        'expenses': all_expenses
    }

    return render(request, template, d)


@login_required
@staff_member_required
def expense_details(request, expense_id=None, template='fidouche/expense_details.html'):
    """Show/edit single expense"""
    expense_id = int(expense_id)
    expense = get_object_or_404(Expense, pk=expense_id)

    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>KA-CHING.</strong> Expense edited.')
            return redirect(request.path)
    else:
        form = ExpenseForm(instance=expense)

    d = {
        'form': form,
        'expense': expense
    }

    return render(request, template, d)


@login_required
@staff_member_required
def expense_create(request, template='fidouche/expense_create.html'):
    """Create a new expense record"""

    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)
        form.save()
        messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>KA-CHING.</strong> Expense added.')
        if request.POST.get('date'):
            year = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').year
            return redirect(expenses_list, year)
        return redirect(all_expenses_list)

    else:
        form = ExpenseForm()
        expense = None

    d = {
        'form': form,
        'expense': expense
    }

    return render(request, template, d)


@login_required
@staff_member_required
def expense_delete(request, expense_id=None):
    """Delete an expense record"""
    expense_id = int(expense_id)
    expense = get_object_or_404(Expense, pk=expense_id)
    expense_date = None
    if expense.show:
        expense_date = expense.show.date
    if expense.date:
        expense_date = expense.date
    if expense_id:
        expense.delete()
        messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>Toast.</strong> Expense deleted.')
    else:
        messages.add_message(request, messages.WARNING, '<i class="fa fa-warning"></i> <strong>HUH?</strong> That\'s not a thing.')
    if expense_date:
        return redirect(expenses_list, expense_date.year)
    else:
        return redirect(all_expenses_list)

@login_required
def income_list(request, year=current_year, template='fidouche/income_list.html'):
    """Show non-gig income"""
    incomes = Income.objects.filter(date__year=year)
    d = {
        'incomes': incomes
    }

    return render(request, template, d)


@login_required
def all_income_list(request, template='fidouche/income_list.html'):
    """Show non-gig expenses"""
    incomes = Income.objects.all()

    d = {
        'incomes': incomes
    }

    return render(request, template, d)


@login_required
@staff_member_required
def income_details(request, income_id=None, template='fidouche/income_details.html'):
    """Show/edit single income"""
    income_id = int(income_id)
    income = get_object_or_404(Income, pk=income_id)

    if request.method == "POST":
        form = IncomeForm(request.POST, request.FILES, instance=income)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>KA-CHING.</strong> Income edited.')
            return redirect(request.path)
    else:
        form = IncomeForm(instance=income)

    d = {
        'form': form,
        'income': income
    }

    return render(request, template, d)


@login_required
@staff_member_required
def income_create(request, template='fidouche/income_create.html'):
    """Create a new income record"""

    if request.method == "POST":
        form = IncomeForm(request.POST, request.FILES)
        form.save()
        messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>KA-CHING.</strong> Income added.')
        if request.POST.get('date'):
            year = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').year
            return redirect(income_list, year)
        return redirect(all_income_list)

    else:
        form = IncomeForm()
        income = None

    d = {
        'form': form,
        'income': income
    }

    return render(request, template, d)


@login_required
@staff_member_required
def income_delete(request, income_id=None):
    """Delete an income record"""
    income_id = int(income_id)
    income = get_object_or_404(Income, pk=income_id)
    income_date = None
    if income.date:
        income_date = income.date
    if income_id:
        income.delete()
        messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>Toast.</strong> Income deleted.')
    else:
        messages.add_message(request, messages.WARNING, '<i class="fa fa-warning"></i> <strong>HUH?</strong> That\'s not a thing.')
    if income_date:
        return redirect(income_list, income_date.year)
    else:
        return redirect(all_income_list)


@login_required
def finance_reports(request, template='fidouche/finance_reports.html'):
    """View finance reports for a given timeframe"""

    d = {
        'no_dates': False
    }
    start = request.GET.get('start_date', None)
    end = request.GET.get('end_date', None)
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        d['start_date'] = start_date
        d['end_date'] = end_date

        member_payments = {}
        memberPayments = Payment.objects.filter(show__date__range=(start_date, end_date)).filter(paid=True).filter(amount__gt=0)
        for payment in memberPayments:
            if payment.member in member_payments:
                member_payments[payment.member]['total'].append(payment.amount)
                member_payments[payment.member]['payments'].append(payment)
            else:
                member_payments[payment.member] = {
                    'total': [payment.amount],
                    'payments': [payment]
                }
        for member in member_payments:
            member_payments[member]['total'] = sum(member_payments[member]['total'])
        d.update({'member_payments': member_payments})

        sub_payments = {}
        subPayments = SubPayment.objects.filter(show__date__range=(start_date, end_date)).filter(paid=True).filter(amount__gt=0)
        for payment in subPayments:
            if payment.sub in sub_payments:
                sub_payments[payment.sub]['total'].append(payment.amount)
                sub_payments[payment.sub]['payments'].append(payment)
            else:
                sub_payments[payment.sub] = {
                    'total': [payment.amount],
                    'payments': [payment]
                }
        for sub in sub_payments:
            sub_payments[sub]['total'] = sum(sub_payments[sub]['total'])
        d.update({
            'sub_payments': sub_payments,
        })

        expense_payments = {}
        expensePayments = Expense.objects.filter(date__range=(start_date, end_date)).filter(amount__gt=0)
        tourExpensePayments = TourExpense.objects.filter(date__range=(start_date, end_date)).filter(amount__gt=0)
        allExpenses = list(chain(expensePayments, tourExpensePayments))
        for payment in allExpenses:
            if payment.payee in expense_payments:
                expense_payments[payment.payee]['total'].append(payment.amount)
                expense_payments[payment.payee]['payments'].append(payment)
            else:
                expense_payments[payment.payee] = {
                    'total': [payment.amount],
                    'payments': [payment]
                }
        for payee in expense_payments:
            expense_payments[payee]['total'] = sum(expense_payments[payee]['total'])

        d.update({'expense_payments': expense_payments})

    else:
        d['no_dates'] = True
        d['last_year'] = date.today().year - 1

    return render(request, template, d)


@login_required
def tax_reports(request, template='fidouche/tax_reports.html'):
    """View finance reports for a given timeframe"""

    d = {
        'no_dates': False
    }
    start = request.GET.get('start_date', None)
    end = request.GET.get('end_date', None)
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()

        d['start_date'] = start_date
        d['end_date'] = end_date
        # All payments for the date range
        payments = Payment.objects.filter(show__date__range=(start_date, end_date)).filter(paid=True).filter(amount__gt=0)

        # PARTNER PAYMENTS aka "Guaranteed Payments"
        # We want all payments to members who were partners during this time period.
        # Get everyone who has been a partner, ie, they joined at some point
        partners = Member.objects.filter(date_partner_joined__isnull=False)
        # Exclude everyone who became a partner after the end date
        # Exclude everyone who left the partnership before the start date
        partners = partners.exclude(date_partner_joined__gt=end_date).exclude(date_partner_left__lt=start_date)
        partnerPayments = payments.filter(member__in=partners)
        partner_payments = {}
        partner_total = []
        all_partners_total = []
        for payment in partnerPayments:
            partner_total.append(payment.amount)
            all_partners_total.append(payment.amount)
            if payment.member in partner_payments:
                partner_payments[payment.member]['total'].append(payment.amount)
                partner_payments[payment.member]['payments'].append(payment)
            else:
                partner_payments[payment.member] = {
                    'total': [payment.amount],
                    'payments': [payment]
                }
        for member in partner_payments:
            partner_payments[member]['total'] = sum(partner_payments[member]['total'])
        partner_total = sum(partner_total)
        d.update({
            'partner_payments': partner_payments,
            'partner_total': partner_total,
            'all_partners_total': sum(all_partners_total)
            })

        # NON-partner payments, ie, subs and non-partner members
        non_partner_payments = {}
        subPayments = SubPayment.objects.filter(show__date__range=(start_date, end_date)).filter(paid=True).filter(amount__gt=0)
        nonPartnerPayments = payments.exclude(id__in=partnerPayments)
        non_partners_total = []
        for payment in subPayments:
            non_partners_total.append(payment.amount)
            if payment.sub in non_partner_payments:
                non_partner_payments[payment.sub]['total'].append(payment.amount)
                non_partner_payments[payment.sub]['payments'].append(payment)
            else:
                non_partner_payments[payment.sub] = {
                    'total': [payment.amount],
                    'payments': [payment]
                }

        for payment in nonPartnerPayments:
            non_partners_total.append(payment.amount)
            if payment.member in non_partner_payments:
                non_partner_payments[payment.member]['total'].append(payment.amount)
                non_partner_payments[payment.member]['payments'].append(payment)
            else:
                non_partner_payments[payment.member] = {
                    'total': [payment.amount],
                    'payments': [payment]
                }

        for person in non_partner_payments:
            person.type = person.__class__.__name__
            non_partner_payments[person]['total'] = sum(non_partner_payments[person]['total'])

        d.update({
            'non_partner_payments': non_partner_payments,
            'non_partners_total': sum(non_partners_total)
        })

        expense_payments = {}
        expensePayments = Expense.objects.filter(date__range=(start_date, end_date)).filter(amount__gt=0)
        tourExpensePayments = TourExpense.objects.filter(date__range=(start_date, end_date)).filter(amount__gt=0)
        allExpenses = list(chain(expensePayments, tourExpensePayments))
        for payment in allExpenses:
            if payment.new_category.tax_category.name in expense_payments:
                expense_payments[payment.new_category.tax_category.name]['total'].append(payment.amount)
                expense_payments[payment.new_category.tax_category.name]['payments'].append(payment)
            else:
                expense_payments[payment.new_category.tax_category.name] = {
                    'total': [payment.amount],
                    'payments': [payment]
                }
        for category in expense_payments:
            expense_payments[category]['total'] = sum(expense_payments[category]['total'])
            expense_payments[category]['show'] = True

        d.update({
            'expense_payments': expense_payments
        })

        production_payments = ProductionPayment.objects.filter(show__date__range=(start_date, end_date)).filter(paid=True).filter(amount__gt=0).order_by('show__date')
        total_production_payments = []
        for payment in production_payments:
            total_production_payments.append(payment.amount)

        d.update({
            'production_payments': production_payments,
            'total_production_payments': sum(total_production_payments)
        })

        # this is the data structure we're going for here.
        # vendors = {
        #     payee: {
        #         total: [1, 2, 3],
        #         categories: {
        #             category: [1,2,3]
        #         },
        #         payments: [<payment>, <payment>]
        #     }
        # }
        vendors = {}
        vendors_total = []
        allPayments = list(chain(expensePayments, tourExpensePayments, production_payments))
        for expense in allPayments:
            vendors_total.append(expense.amount)
            if expense.payee in vendors:
                vendors[expense.payee]['total'].append(expense.amount)
            else:
                vendors[expense.payee] = {
                    'total': [expense.amount],
                    'categories': {},
                    'payments': [],
                    'type': expense.payee.__class__.__name__
                }
            if expense.new_category.tax_category.name in vendors[expense.payee]['categories']:
                vendors[expense.payee]['categories'][expense.new_category.tax_category.name].append(expense.amount)
            else:
                vendors[expense.payee]['categories'][expense.new_category.tax_category.name] = [expense.amount]
            vendors[expense.payee]['payments'].append(expense)
        for vendor in vendors:
            vendors[vendor]['total'] = sum(vendors[vendor]['total'])
            for category in vendors[vendor]['categories']:
                vendors[vendor]['categories'][category] = sum(vendors[vendor]['categories'][category])

        d.update({
            'vendor_payments': vendors,
            'all_vendors_total': sum(vendors_total)
        })

        commission_payments = CommissionPayment.objects.filter(show__date__range=(start_date, end_date)).filter(paid=True).filter(amount__gt=0).order_by('show__date')
        total_commission_payments = []
        for payment in commission_payments:
            total_commission_payments.append(payment.amount)
        d.update({
            'commission_payments': commission_payments,
            'total_commission_payments': sum(total_commission_payments)
        })

        # Income
        shows = Show.objects.filter(date__range=(start_date, end_date))
        paid_by_client = shows.filter(payer='client')
        paid_by_client_total_gross = []
        for show in paid_by_client:
            if show.gross:
                paid_by_client_total_gross.append(show.gross)
        d['paid_by_client'] = paid_by_client
        d['paid_by_client_total_gross'] = sum(paid_by_client_total_gross)

        paid_by_agent = shows.exclude(id__in=paid_by_client)
        paid_by_agent_total_gross = []
        for show in paid_by_agent:
            if show.commission_withheld:
                show.adjusted_gross = show.gross - show.commission
                paid_by_agent_total_gross.append(show.adjusted_gross)
            else:
                paid_by_agent_total_gross.append(show.gross)

        d['paid_by_agent'] = paid_by_agent
        d['paid_by_agent_total_gross'] = sum(paid_by_agent_total_gross)

        other_income = Income.objects.filter(date__range=(start_date, end_date))
        d['other_income'] = other_income
        d['total_other_income'] = sum([income.amount for income in other_income])

        d['total_income'] = sum(paid_by_agent_total_gross) + sum(paid_by_client_total_gross) + sum([income.amount for income in other_income])

    else:
        d['no_dates'] = True

    d['last_year'] = date.today().year - 1

    return render(request, template, d)


@login_required
def member_payments(request, member_id=None,  template='fidouche/payments.html'):
    """View finance reports for a given timeframe/member"""
    member_id = int(member_id)
    member = Member.objects.get(pk=member_id)
    d = {
        'no_dates': False
    }
    start = request.GET.get('start_date', None)
    end = request.GET.get('end_date', None)
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        d['start_date'] = start_date
        d['end_date'] = end_date
        # All payments for the date range
        payment_totals = []
        payments = Payment.objects.filter(show__date__range=(start_date, end_date)).filter(member=member, amount__gt=0)
        for payment in payments:
            payment_totals.append(payment.amount)
        d['payments'] = payments
        d['payee'] = member
        d['total'] = sum(payment_totals)
    else:
        d['no_dates'] = True

    return render(request, template, d)


@login_required
def sub_payments(request, sub_id=None,  template='fidouche/payments.html'):
    """View finance reports for a given timeframe/member"""
    sub_id = int(sub_id)
    sub = Sub.objects.get(pk=sub_id)
    d = {
        'no_dates': False
    }
    start = request.GET.get('start_date', None)
    end = request.GET.get('end_date', None)
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        d['start_date'] = start_date
        d['end_date'] = end_date
        # All payments for the date range
        payment_totals = []
        payments = SubPayment.objects.filter(show__date__range=(start_date, end_date)).filter(sub=sub, amount__gt=0)
        for payment in payments:
            payment_totals.append(payment.amount)
        d['payments'] = payments
        d['payee'] = sub
        d['total'] = sum(payment_totals)
    else:
        d['no_dates'] = True

    return render(request, template, d)


@login_required
def vendor_payments(request, vendor_id=None,  template='fidouche/vendor_payments.html'):
    """View finance reports for a given timeframe/member"""
    vendor_id = int(vendor_id)
    vendor = Payee.objects.get(pk=vendor_id)
    d = {
        'no_dates': False
    }
    start = request.GET.get('start_date', None)
    end = request.GET.get('end_date', None)
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        d['start_date'] = start_date
        d['end_date'] = end_date
        # All payments for the date range
        payment_totals = []
        expense_payments = Expense.objects.filter(date__range=(start_date, end_date)).filter(payee=vendor, amount__gt=0)
        tour_payments = TourExpense.objects.filter(date__range=(start_date, end_date)).filter(payee=vendor, amount__gt=0)
        payments = list(chain(expense_payments, tour_payments))
        for payment in payments:
            payment_totals.append(payment.amount)
        d['payments'] = payments
        d['payee'] = vendor
        d['total'] = sum(payment_totals)
    else:
        d['no_dates'] = True

    return render(request, template, d)


@login_required
def production_payments(request, company_id=None,  template='fidouche/vendor_payments.html'):
    """View finance reports for a given timeframe/member"""
    vendor_id = int(company_id)
    vendor = ProductionCompany.objects.get(pk=vendor_id)
    d = {
        'no_dates': False
    }
    start = request.GET.get('start_date', None)
    end = request.GET.get('end_date', None)
    if start and end:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        d['start_date'] = start_date
        d['end_date'] = end_date
        # All payments for the date range
        payment_totals = []
        payments = ProductionPayment.objects.filter(show__date__range=(start_date, end_date)).filter(company=vendor, amount__gt=0)
        for payment in payments:
            payment_totals.append(payment.amount)
        d['payments'] = payments
        d['payee'] = vendor
        d['total'] = sum(payment_totals)
    else:
        d['no_dates'] = True

    return render(request, template, d)


@login_required
def tour_list(request, template='fidouche/tour_list.html'):
    """View all tours"""
    d = {}
    tours = Tour.objects.all()
    d['tours'] = tours

    return render(request, template, d)


@login_required
def tour_detail(request, tour_id=None, template='fidouche/tour_detail.html'):
    """View tour"""
    ExpenseFormSet = inlineformset_factory(Tour, TourExpense, form=TourExpenseForm)
    d = {}
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == "POST":

        expense_formset = ExpenseFormSet(request.POST, request.FILES, instance=tour)
        if expense_formset.is_valid():
            expense_formset.save()
            messages.add_message(request, messages.SUCCESS, '<i class="fa fa-beer"></i> <strong>NICE.</strong> Tour finances updated!')
            return redirect(request.path)
        else:
            messages.add_message(request, messages.ERROR, '<i class="fa fa-wrench"></i> <strong>Aw, damnit.</strong> Something\'s fucked up.')
    else:
        expense_formset = ExpenseFormSet(instance=tour)

    d = {
        'tour': tour,
        'expense_formset': expense_formset,
        'maps_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, template, d)


@login_required
def venue_map(request, template='fidouche/venue_map.html'):

    d = {
        'venues': Venue.objects.exclude(ltlng=''),
        'maps_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, template, d)


def venue_map_data(request):
    venue_set = Venue.objects.exclude(ltlng='')
    venue_set = [v for v in venue_set if v.shows.all()]
    venues = sorted(venue_set, key=lambda v: v.first_show)
    venue_data = []
    for venue in venues:
        venue_ltlng = list([float(x) for x in venue.ltlng.split(',')])
        venue_image_url = None
        venue_net = 0
        venue_average = 0
        shows = venue.shows.all()
        net_shows = [show for show in shows if show.net]
        if venue.venue_image:
            venue_image_url = venue.venue_image.url
        if net_shows:
            venue_net = int(sum([show.net for show in net_shows]))
            venue_average = int(sum([show.net for show in net_shows])) / len(net_shows)
        venue_data.append({
            'coordinates': venue_ltlng,
            'name': venue.venue_name,
            'city': venue.city,
            'state': venue.state,
            'image': venue_image_url,
            'shows': [show.date.strftime('%m/%d/%Y') for show in shows],
            'net_display': intcomma(venue_net),
            'net': max(venue_net, 0),
            'average': max(venue_average, 0),
            'average_display': intcomma(venue_average),
            'num_shows': len(shows),
            'first_show_year': venue.first_show_year
        })

    return HttpResponse(json.dumps(venue_data), content_type="application/json")
