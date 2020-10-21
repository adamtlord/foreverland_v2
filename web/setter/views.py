from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from shows.models import Show
from songs.models import Song, Setlist, SetlistSong


@login_required
def setter_dashboard(request, template='setter/dashboard.html'):
    """"""
    
    songs = Song.objects.filter(display=True)
    setlists = Setlist.objects.all()

    d = {
        'songs': songs,
        'setlists': setlists,
    }
    return render(request, template, d)

@login_required
def view_setlist(request, gig_id=None, template='setter/view_setlist.html'):
    """View the setlist from a given show"""

    gig_id = int(gig_id)
    gig = get_object_or_404(Show, pk=gig_id)
    setlist = gig.setlist.all()[:1].get()
    setsongs = SetlistSong.objects.filter(setlist=setlist).order_by('order')

    d = {
        'gig': gig,
        'setsongs': setsongs
    }
    return render(request, template, d)

