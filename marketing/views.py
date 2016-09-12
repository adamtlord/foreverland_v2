import datetime

from django.shortcuts import render, redirect

from members.models import Member
from shows.models import Show
from media.models import Video
from marketing.models import Testimonial


def homepage(request, template='marketing/homepage.html'):
    """Returns homepage.html for the root url"""
    feed = request.GET.get('feed', None)
    if feed == 'gigpress':
        return redirect('/shows/rss')
    if feed == 'gigpress-ical':
        return redirect('/shows/ical')
    public_shows = Show.objects.filter(public=True)
    next_show = public_shows.filter(date__gte=datetime.datetime.now()).order_by('date')[0]
    members = Member.objects.filter(active=True).order_by('display_last')
    vocals = members.filter(active=True, section='v')
    horns = members.filter(active=True, section='h')
    rhythm = members.filter(active=True, section='r')
    tonight = datetime.datetime.date(next_show.date) == datetime.datetime.today().date()
    if tonight:
        tonight = 'tonight' if next_show.date.hour >= 17 else 'today'

    d = {}
    d['next_show'] = next_show
    d['vocals'] = vocals
    d['horns'] = horns
    d['rhythm'] = rhythm
    d['tonight'] = tonight

    return render(request, template, d)


def about(request, template='marketing/about.html'):
    """Featured Testimonials"""
    testimonials = Testimonial.objects.all().order_by('?')

    d = {
        'quotes': testimonials
    }

    return render(request, template, d)


def faq(request, template='marketing/faq.html'):
    """FAQ page"""

    return render(request, template)


def video(request, template='marketing/video.html'):
    """Video page"""
    featured_videos = Video.objects.filter(featured=True)

    d = {
        'featured_videos': featured_videos
    }
    return render(request, template, d)


def booking(request, template='marketing/booking.html'):
    """Booking/Contact page"""

    return render(request, template)