import datetime
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from django_ical.views import ICalFeed

from shows.models import Show


class CalendarFeed(ICalFeed):
	"""An iCal feed of upcoming events"""
	product_id = '-//Foreverland//Band//EN'
	timezone = 'America/Los_Angeles'
	title = 'Foreverland Upcoming Shows'

	def items(self):
		return Show.objects.filter(public=True).filter(date__gte=datetime.datetime.now()).order_by('date')

	def item_title(self, item):
		return '%s, %s - %s' % (item.venue, item.venue.city, item.date.strftime('%I:%M %p'))

	def item_description(self, item):
		time = 'Show at %s\n' % item.date.strftime('%I:%M %p')
		price = ''
		ages = ''
		notes = ''
		if item.doors_time:
			time += 'Doors at %s\n' % item.doors_time.strftime('%I:%M %p')
		if item.ticket_price:
			price = 'Ticket price: %s\n' % item.ticket_price
		if item.ages:
			ages = 'Ages: %s\n' % item.ages
		if item.notes:
			notes = item.notes
		return '%s%s%s%s' % (time, price, ages, notes)

	def item_start_datetime(self, item):
		return item.date

	def item_link(self, item):
		return '/shows/%s/' % (item.id)

	def item_class(self):
		return 'PUBLIC'

	def item_location(self, item):
		loc = item.venue.address1
		if item.venue.address2:
			loc += ', ' + item.venue.address2
		if item.venue.zip_code:
			loc += ', ' + item.venue.zip_code
		return loc


class ShowsFeed(Feed):
	"""An RSS feed of upcoming events"""
	title = 'Foreverland'
	link = '/shows/'
	description = 'Upcoming Shows'

	def items(self):
		return Show.objects.filter(public=True).filter(date__gte=datetime.datetime.now()).order_by('date')

	def item_title(self, item):
		return '%s, %s - %s' % (item.venue, item.venue.city, item.date.strftime('%I:%M %p'))

	def item_link(self, item):
		return reverse('show', args=[item.pk])
	
	def item_description(self, item):
		time = 'Show at %s\n' % item.date.strftime('%I:%M %p')
		price = ''
		ages = ''
		notes = ''
		if item.doors_time:
			time += 'Doors at %s\n' % item.doors_time.strftime('%I:%M %p')
		if item.ticket_price:
			price = 'Ticket price: %s\n' % item.ticket_price
		if item.ages:
			ages = 'Ages: %s\n' % item.ages
		if item.notes:
			notes = item.notes

		return '%s%s%s%s' % (time, price, ages, notes)
