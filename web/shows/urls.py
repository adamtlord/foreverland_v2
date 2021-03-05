from django.urls import path

from shows.feeds import CalendarFeed, ShowsFeed
from shows.views import upcoming_shows, past_shows, show, show_modal


urlpatterns = [
    path("", upcoming_shows, {}, name="upcoming_shows"),
    path("past/", past_shows, {}, name="past_shows"),
    path("<int:show_id>/", show, {}, name="show"),
    path("modal/<int:show_id>/", show_modal, {}, name="show_modal"),
    path("ical/", CalendarFeed()),
    path("rss/", ShowsFeed()),
]
