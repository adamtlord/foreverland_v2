from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from shows.models import Show
from songs.models import Setlist, SetlistSong, Song


@login_required
def setter_dashboard(request, template="setter/dashboard.html"):
    """"""

    songs = Song.objects.filter(display=True)
    setlists = (
        Setlist.objects.select_related("show__venue")
        .annotate(song_count=Count("songs"))
        .order_by("-show__date")
    )

    d = {
        "songs": songs,
        "setlists": setlists,
    }
    return render(request, template, d)


@login_required
def view_setlist(request, gig_id=None, template="setter/view_setlist.html"):
    """View the setlist from a given show"""

    gig_id = int(gig_id)
    gig = get_object_or_404(Show.objects.select_related("venue"), pk=gig_id)
    setlist = get_object_or_404(Setlist, show=gig)
    setsongs = (
        SetlistSong.objects.filter(setlist=setlist)
        .select_related("song")
        .order_by("order")
    )

    d = {"gig": gig, "setsongs": setsongs}
    return render(request, template, d)
