import csv
import datetime
from decimal import Decimal
from dateutil import parser
from django.core.management.base import BaseCommand
from shows.models import Show

# insert path to csv file to import here
# CSV_FILE = '/home/adamlord/webapps/foreverland_python/src/foreverland/apps/fidouche/csv/gigs12.csv'

class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(CSV_FILE) as csvfile:
            gigs = csv.reader(csvfile)
            gigs.next()
            for row in gigs:
                date = parser.parse(row[0])
                show = Show.objects.filter(date__range=(datetime.datetime.combine(date, datetime.time.min),datetime.datetime.combine(date, datetime.time.max)))
                if show:
                    show = show[0]
                    show.gross = self.__string_to_decimal(row[2])
                    show.commission = self.__string_to_decimal(row[3])
                    show.sound_cost = self.__string_to_decimal(row[4])
                    show.in_ears_cost = self.__string_to_decimal(row[5])
                    show.print_ship_cost = self.__string_to_decimal(row[6])
                    show.ads_cost = self.__string_to_decimal(row[7])
                    show.other_cost = self.__string_to_decimal(row[8])
                    show.net = self.__string_to_decimal(row[9])
                    show.payout = self.__string_to_decimal(row[10])
                    show.to_account = self.__string_to_decimal(row[11])
                    show.save()
                else:
                    print 'no show for %s found in db' % date
    
    def __string_to_decimal(self, string):
        if string:
            return Decimal(string)
        else:
            return 0
