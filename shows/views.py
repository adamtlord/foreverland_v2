import datetime
from django.shortcuts import render, get_object_or_404
from shows.models import Show

UPCOMING_WINDOW_WEEKS = 12

def upcoming_shows(request, template='shows/upcoming.html'):
    """list all upcoming shows for the next n weeks"""
    startdate = datetime.datetime.now()
    enddate = startdate + datetime.timedelta(weeks=UPCOMING_WINDOW_WEEKS)
    
    public_shows = Show.objects.filter(public=True)
    upcoming_shows = public_shows.filter(date__range=[startdate, enddate]).order_by('date')
    
    d = {}
    d['shows'] = upcoming_shows
    return render(request, template, d)

def past_shows(request, template='shows/past.html'):
    """list all past shows"""
    public_shows = Show.objects.filter(public=True)
    past_shows = public_shows.filter(date__lt=datetime.datetime.now()).order_by('date')
    shows_by_year = {}
    for show in past_shows:
    	if show.date.year not in shows_by_year:
    		shows_by_year[show.date.year] = []
    	shows_by_year[show.date.year].append(show)
    show_years = [x for x in shows_by_year]

    d = {}
    d['shows_by_year'] = shows_by_year
    d['show_years'] = show_years
    return render(request, template, d)

def show(request, show_id, template='shows/detail.html'):
	"""display individual show"""
	show = get_object_or_404(Show, pk=show_id)
	return render(request, template, {'show':show})

def show_modal(request, show_id, template='shows/modal.html'):
	"""display individual show"""
	show = get_object_or_404(Show, pk=show_id)
	return render(request, template, {'show':show})
