import datetime
from django.core.management.base import BaseCommand, CommandError

from legacy.models import WpRandomtext, WpGigpressVenues, WpGigpressShows
from marketing.models import Testimonial
from shows.models import Venue, Show

class Command(BaseCommand):
	def handle(self, *args, **options):
		print 'migrate testimonials'
		rts = WpRandomtext.objects.using('legacy').all()
		for rt in rts:
			t = Testimonial(quote=rt.text, featured=True)
			t.save()

		print 'migrate venues'
		gpvs = WpGigpressVenues.objects.using('legacy').all()
		for gpv in gpvs:
			v = Venue(id=gpv.venue_id, 
				venue_name=gpv.venue_name, 
				venue_image='venues/%s' % gpv.venue_phone,
				address1=gpv.venue_address,
				city=gpv.venue_city,
				state=gpv.venue_state,
				zip_code=gpv.venue_postal_code,
				website=gpv.venue_url)
			v.save()

		print 'migrate shows'
		gps = WpGigpressShows.objects.using('legacy').all()
		for gp in gps:
			try:
				d = datetime.datetime.combine(gp.show_date, gp.show_time)
				venue = Venue.objects.filter(id=gp.show_venue_id)[0]

				if gp.show_ages == 'Not sure':
					ages = ''
				else:
					ages = gp.show_ages

				public = True
				if venue.venue_name == 'Private Event':
					public = False

				s = Show(
					public=public,
					date=d, 
					venue=venue,
					ticket_price=gp.show_price,
					ticket_url=gp.show_tix_url,
					ages=ages,
					notes=gp.show_notes
					)
				s.save()
			except IndexError:
				pass