from django.core.management.base import BaseCommand
from datetime import date

from shows.models import Show
from fidouche.models import Agent, CommissionPayment

today = date.today()

def get_default_agent():
    agents = Agent.objects.all()
    if agents.count():
        return agents[0]
    else:
        return None


class Command(BaseCommand):
    def handle(self, *args, **options):
        agent = get_default_agent()
        shows = Show.objects.all()
        if agent:
            print 'agent: %s' % agent
            for show in shows:
                print 'show: %s' % show
                if show.commission and not show.commission_withheld:
                    past = show.date.date() <= today
                    commission_payment, created = CommissionPayment.objects.get_or_create(show=show)
                    if created:
                        print '- creating commission payment'
                        print '- commission: %s' % show.commission
                    else:
                        print '-- alread created, updating'
                    commission_payment.agent=agent
                    commission_payment.amount=show.commission
                    commission_payment.paid=past
                    commission_payment.check_no=show.commission_check_no
                    commission_payment.save()
                else:
                    if not show.commission:
                        print 'xx no commission'
                    else:
                        print 'xx commission_withheld'
        else:
            print '!!! Update the DB first !!!!'




