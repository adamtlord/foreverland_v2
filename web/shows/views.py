import datetime
from collections import OrderedDict

from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from shows.models import Show

UPCOMING_WINDOW_WEEKS = 16


def upcoming_shows(request, template="shows/upcoming.html"):
    """list all upcoming shows for the next n weeks"""
    startdate = datetime.datetime.now()
    enddate = startdate + datetime.timedelta(weeks=UPCOMING_WINDOW_WEEKS)

    public_shows = Show.objects.filter(public=True).select_related("venue")
    upcoming_shows = public_shows.filter(date__range=[startdate, enddate]).order_by(
        "date"
    )

    d = {}
    d["shows"] = upcoming_shows
    return render(request, template, d)


def past_shows(request, template="shows/past.html"):
    """List past shows, defaulting to the latest year."""
    from common.utils import years_with_gigs

    show_years = years_with_gigs()
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = None
    if not year:
        year = show_years[-1] if show_years else None

    public_shows = Show.objects.filter(public=True).select_related("venue")
    past_qs = public_shows.filter(date__lt=datetime.datetime.now()).order_by("date")
    if year:
        past_qs = past_qs.filter(date__year=year)

    shows_by_year = OrderedDict()
    for show in past_qs:
        shows_by_year.setdefault(show.date.year, []).append(show)

    return render(
        request,
        template,
        {
            "shows_by_year": shows_by_year,
            "show_years": show_years,
            "selected_year": year,
        },
    )


def show(request, show_id, template="shows/detail.html"):
    """display individual show"""
    show = get_object_or_404(Show.objects.select_related("venue"), pk=show_id)
    return render(request, template, {"show": show})


def show_modal(request, show_id, template="shows/modal.html"):
    """display individual show"""
    show = get_object_or_404(Show.objects.select_related("venue"), pk=show_id)
    return render(request, template, {"show": show})


class TheWorksView(TemplateView):
    template_name = "shows/theworks.html"
