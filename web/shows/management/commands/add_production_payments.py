from django.core.management.base import BaseCommand
from datetime import date

from shows.models import Show
from fidouche.models import ProductionPayment, ProductionCategory, ProductionCompany

today = date.today()

def get_default_company():
    companies = ProductionCompany.objects.all()
    if companies.count():
        return companies[0]
    else:
        return None

def get_iem_catetory():
    categories = ProductionCategory.objects.filter(name='IEM')
    if categories.count():
        return categories[0]
    else:
        return None

def get_sound_category():
    categories = ProductionCategory.objects.filter(name='Sound')
    if categories.count():
        return categories[0]
    else:
        return None


class Command(BaseCommand):
    def handle(self, *args, **options):
        company = get_default_company()
        iem_cat = get_iem_catetory()
        sound_cat = get_sound_category()

        shows = Show.objects.all()

        if company and iem_cat and sound_cat:
            print 'company: %s' % company
            for show in shows:
                print 'show: %s' % show
                if show.in_ears_cost or show.sound_cost:
                    past = show.date.date() <= today
                    if show.in_ears_cost:
                        iem_production_payment, created = ProductionPayment.objects.get_or_create(show=show, category=iem_cat, amount=show.in_ears_cost, company=company)
                        if created:
                            print '- creating IEM payment'
                            print '- amount: %s' % show.in_ears_cost
                        else:
                            print '-- alread created, updating'
                        iem_production_payment.company=company
                        iem_production_payment.amount=show.in_ears_cost
                        iem_production_payment.paid=past
                        iem_production_payment.check_no=show.in_ears_check_no
                        iem_production_payment.save()
                    if show.sound_cost:
                        sound_production_payment, created = ProductionPayment.objects.get_or_create(show=show, category=sound_cat, amount=show.sound_cost, company=company)
                        if created:
                            print '- creating sound payment'
                            print '- amount: %s' % show.sound_cost
                        else:
                            print '-- alread created, updating'
                        sound_production_payment.company=company
                        sound_production_payment.amount=show.sound_cost
                        sound_production_payment.paid=past
                        sound_production_payment.check_no=show.sound_check_no
                        sound_production_payment.save()
                else:
                    if not show.in_ears_cost:
                        print 'xx no IEMs'
                    else:
                        print 'xx no Sound Cost'
        else:
            print '!!! Update the DB first !!!!'





