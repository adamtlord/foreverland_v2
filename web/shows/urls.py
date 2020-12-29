from django.conf.urls import url

from shows.feeds import CalendarFeed, ShowsFeed
from shows.views import upcoming_shows, past_shows, show, show_modal


urlpatterns = [
    url(r"^$", upcoming_shows, {}, name="upcoming_shows"),
    url(r"^past/$", past_shows, {}, name="past_shows"),
    url(r"^(?P<show_id>\d+)/$", show, {}, name="show"),
    url(r"^modal/(?P<show_id>\d+)/$", show_modal, {}, name="show_modal"),
    url(r"^ical/$", CalendarFeed()),
    url(r"^rss/$", ShowsFeed()),
]
