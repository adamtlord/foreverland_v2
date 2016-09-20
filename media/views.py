from collections import defaultdict

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from media.models import *
from media.forms import ImageUploadForm


def photos(request, template="media/photos.html"):
    """Photos page"""
    promo_album = Album.objects.get(title="Promotional Photos")
    promo_photos = Image.objects.filter(albums__in=[promo_album]).order_by('id')

    d = {
        'promo_photos': promo_photos
    }

    return render(request, template, d)


def downloads(request, template="media/downloads.html"):
    """Downloads page"""
    downloadables = Download.objects.all()
    for dl in downloadables:
        dl.icon_class = ''
        if dl.extension() in ['.pdf', '.doc']:
            dl.icon_class = 'fa-file-text-o'
        if dl.extension() in ['.jpg', '.png', '.gif']:
            dl.icon_class = 'fa-picture-o'

    d = {
        'downloads': downloadables
    }

    return render(request, template, d)


@login_required
def behind_the_music(request, template="media/behind_the_music.html"):
    """Behind the music page"""
    album = Album.objects.get(pk=3)
    album.images = album.image_set.all()
    album.videos = album.video_set.all()

    d = {
        'album': album
    }

    return render(request, template, d)


@login_required
def upload(request, template="media/upload.html"):
    """(bulk) upload of images"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            for image in request.FILES.getlist('image'):
                new_file = Image(image=image)
                new_file.save()
                new_file.albums = form.cleaned_data['albums']
                new_file.save()
    else:
        form = ImageUploadForm(initial={'albums': [3, ]})

    d = {'form': form}
    return render(request, template, d)


def list(request, template="media/list.html"):
    """Main listing."""
    albums = Album.objects.all()
    if not request.user.is_authenticated():
        albums = albums.filter(public=True)

    paginator = Paginator(albums, 10)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        albums = paginator.page(page)
    except (InvalidPage, EmptyPage):
        albums = paginator.page(paginator.num_pages)

    for album in albums.object_list:
        album.images = album.image_set.all()[:4]

    d = {'albums': albums, 'user': request.user}

    return render(request, template, d)


# def album(request, pk, view="thumbnails", template="media/album.html"):
#     """Album listing."""
#     num_images = 30
#     if view == "full":
#         num_images = 10

#     album = Album.objects.get(pk=pk)
#     images = album.image_set.all()
#     paginator = Paginator(images, num_images)
#     try:
#         page = int(request.GET.get("page", '1'))
#     except ValueError:
#         page = 1

#     try:
#         images = paginator.page(page)
#     except (InvalidPage, EmptyPage):
#         images = paginator.page(paginator.num_pages)

#     # add list of tags as string and list of album objects to each image object
#     for img in images.object_list:
#         tags = [x[1] for x in img.tags.values_list()]
#         img.tag_lst = join(tags, ', ')
#         img.album_lst = [x[1] for x in img.albums.values_list()]

#     d = {
#         'album': album,
#         'images': images,
#         'user': request.user,
#         'view': view,
#         'albums': Album.objects.all()
#     }
#     d.update(csrf(request))

#     return render(request, template, d)


def image(request, pk, template="media/image.html"):
    """Image page."""
    img = Image.objects.get(pk=pk)
    d = {
        'image': img,
        'user': request.user,
        'backurl': request.META["HTTP_REFERER"]
    }

    return render(request, template, d)


def update(request):
    """Update image title, tags, albums."""
    p = request.POST
    images = defaultdict(dict)

    # create dictionary of properties for each image
    for k, v in p.items():
        if k.startswith("title") or k.startswith("tags"):
            k, pk = k.split('-')
            images[pk][k] = v
        elif k.startswith("album"):
            pk = k.split('-')[1]
            images[pk]["albums"] = p.getlist(k)

    # process properties, assign to image objects and save
    for k, d in images.items():
        image = Image.objects.get(pk=k)
        image.title = d["title"]

        # tags - assign or create if a new tag!
        tags = d["tags"].split(', ')
        lst = []
        for t in tags:
            if t: lst.append(Tag.objects.get_or_create(tag=t)[0])
        image.tags = lst

        if "albums" in d:
            image.albums = d["albums"]
        image.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"], dict(media_url=MEDIA_URL))


def search(request, template="media/search.html"):
    """Search, filter, sort images."""
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    p = request.POST
    images = defaultdict(dict)

    # init parameters
    parameters = {}
    keys = "title filename width_from width_to height_from height_to tags view"
    keys = keys.split()
    for k in keys:
        parameters[k] = ''
    parameters["album"] = []

    # create dictionary of properties for each image and a dict of search/filter parameters
    for k, v in p.items():
        if k == "album":
            parameters[k] = [int(x) for x in p.getlist(k)]
        elif k in parameters:
            parameters[k] = v
        elif k.startswith("title") or k.startswith("tags"):
            k, pk = k.split('-')
            images[pk][k] = v
        elif k.startswith("album"):
            pk = k.split('-')[1]
            images[pk]["albums"] = p.getlist(k)

    # save or restore parameters from session
    if page != 1 and "parameters" in request.session:
        parameters = request.session["parameters"]
    else:
        request.session["parameters"] = parameters

    results = update_and_filter(images, parameters)

    # make paginator
    paginator = Paginator(results, 20)
    try:
        results = paginator.page(page)
    except (InvalidPage, EmptyPage):
        request = paginator.page(paginator.num_pages)

    # add list of tags as string and list of album names to each image object
    for img in results.object_list:
        tags = [x[1] for x in img.tags.values_list()]
        img.tag_lst = join(tags, ', ')
        img.album_lst = [x[1] for x in img.albums.values_list()]

    d = dict(results=results, user=request.user, albums=Album.objects.all(), prm=parameters, media_url=MEDIA_URL)
    d.update(csrf(request))

    return render(request, template, d)


def update_and_filter(images, p):
    """Update image data if changed, filter results through parameters and return results list."""
    # process properties, assign to image objects and save
    for k, d in images.items():
        image = Image.objects.get(pk=k)
        image.title = d["title"]
        image.rating = int(d["rating"])

        # tags - assign or create if a new tag!
        tags = d["tags"].split(', ')
        lst = []
        for t in tags:
            if t:
                lst.append(Tag.objects.get_or_create(tag=t)[0])
        image.tags = lst

        if "albums" in d:
            image.albums = d["albums"]
        image.save()

    # filter results by parameters
    results = Image.objects.all()
    if p["title"]       : results = results.filter(title__icontains=p["title"])
    if p["filename"]    : results = results.filter(image__icontains=p["filename"])
    if p["width_from"]  : results = results.filter(width__gte=int(p["width_from"]))
    if p["width_to"]    : results = results.filter(width__lte=int(p["width_to"]))
    if p["height_from"] : results = results.filter(height__gte=int(p["height_from"]))
    if p["height_to"]   : results = results.filter(height__lte=int(p["height_to"]))

    if p["tags"]:
        tags = p["tags"].split(', ')
        lst = []
        for t in tags:
            if t:
                results = results.filter(tags=Tag.objects.get(tag=t))

    if p["album"]:
        lst = p["album"]
        or_query = Q(albums=lst[0])
        for album in lst[1:]:
            or_query = or_query | Q(albums=album)
        results = results.filter(or_query).distinct()
    return results

