from common.utils import get_lat_lng
from django.core.management.base import BaseCommand

from shows.models import Venue

class Command(BaseCommand):
	def handle(self, *args, **options):
		vs = Venue.objects.all()
		for v in vs:
			va = ''
			
			if v.address1:
				va += v.address1
				va += ' '
			if v.address2:
				va += v.address2
				va += ' '
			va += v.city 
			va += ' '
			va += v.state
			va += ' '
			va += v.country

			v.ltlng = get_lat_lng(va)
			print v.id
			v.save(update_fields=['ltlng'])

			
