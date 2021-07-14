from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import render
from media.models import Album, Download, Image


def photos(request, template="media/photos.html"):
    """Photos page"""
    promo_album = Album.objects.get(title="Promotional Photos")
    promo_photos = Image.objects.filter(albums__in=[promo_album]).order_by("id")

    d = {"promo_photos": promo_photos}

    return render(request, template, d)


def downloads(request, template="media/downloads.html"):
    """Downloads page"""
    downloadables = Download.objects.all()
    for dl in downloadables:
        dl.icon_class = ""
        if dl.extension() in [".pdf", ".doc"]:
            dl.icon_class = "fa-file-text-o"
        if dl.extension() in [".jpg", ".png", ".gif"]:
            dl.icon_class = "fa-picture-o"

    d = {"downloads": downloadables}

    return render(request, template, d)


@login_required
def behind_the_music(request, template="media/behind_the_music.html"):
    """Behind the music page"""
    album = Album.objects.get(pk=3)
    album.images = album.image_set.all()
    album.videos = album.video_set.all()

    d = {"album": album}

    return render(request, template, d)
