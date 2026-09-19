from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from media.models import Album, Download, Image


def photos(request, template="media/photos.html"):
    """Photos page"""
    promo_photos = Image.objects.filter(
        albums__title="Promotional Photos"
    ).order_by("id")

    d = {"promo_photos": promo_photos}

    return render(request, template, d)


def downloads(request, template="media/downloads.html"):
    """Downloads page"""
    downloadables = Download.objects.all()
    for dl in downloadables:
        extension = dl.extension()
        dl.icon_class = ""
        if extension in [".pdf", ".doc"]:
            dl.icon_class = "fa-file-text-o"
        if extension in [".jpg", ".png", ".gif"]:
            dl.icon_class = "fa-picture-o"

    d = {"downloads": downloadables}

    return render(request, template, d)


@login_required
def behind_the_music(request, template="media/behind_the_music.html"):
    """Behind the music page"""
    album = Album.objects.prefetch_related("image_set", "video_set").get(pk=3)
    album.images = album.image_set.all()
    album.videos = album.video_set.all()

    d = {"album": album}

    return render(request, template, d)
