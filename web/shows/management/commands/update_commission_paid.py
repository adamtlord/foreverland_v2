from django.core.management.base import BaseCommand
from datetime import datetime

from shows.models import Show

now = datetime.now()

class Command(BaseCommand):
    def handle(self, *args, **options):
        shows = Show.objects.filter(date__lte=now)
        for show in shows:
            if show.commission and not show.commission_withheld:
                show.commission_paid = True
                show.save()



