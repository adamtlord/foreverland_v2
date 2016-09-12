import os
from string import join

from django.db import models
from django.conf import settings
from sorl.thumbnail import ImageField

from shows.models import Show


class Album(models.Model):
    title = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    show = models.ManyToManyField(Show, blank=True)

    def __unicode__(self):
        return self.title

    def images(self):
        lst = [x.image.name for x in self.image_set.all()]
        lst = ["<a href='%s/%s'>%s</a>" % (settings.MEDIA_URL, x, x.split('/')[-1]) for x in lst]
        return join(lst, ', ')
    images.allow_tags = True

    def videos(self):
        lst = [x.video.name for x in self.image_set.all()]
        lst = ["<a href='%s/%s'>%s</a>" % (settings.MEDIA_URL, x, x.split('/')[-1]) for x in lst]
        return join(lst, ', ')
    images.allow_tags = True


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    def __unicode__(self):
        return self.tag


class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = ImageField(upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True)
    show = models.ManyToManyField(Show, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    def size(self):
        """Image size"""
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
        return self.image.name

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        return str(join(lst, ', '))

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return str(join(lst, ', '))

    def thumbnail_(self):
        return "<img border='0' alt='' src='%s/%s' height='40' />" % (
                                                                        (settings.MEDIA_URL, self.image.name))
    thumbnail_.allow_tags = True


class Video(models.Model):
    YOUTUBE = 'yt'
    FACEBOOK = 'fb'
    VIMEO = 'vm'
    OTHER = 'o'
    EMBED_TYPES = (
        (YOUTUBE, 'YouTube'),
        (FACEBOOK, 'Facebook'),
        (VIMEO, 'Vimeo'),
        (OTHER, 'other')
    )
    title = models.CharField(max_length=60, blank=True, null=True)
    url = models.URLField()
    vid_id = models.CharField(max_length=100, blank=True, null=True)
    embed_type = models.CharField(max_length=10, blank=True, null=True, choices=EMBED_TYPES, default=YOUTUBE)
    tags = models.ManyToManyField(Tag, blank=True)
    show = models.ManyToManyField(Show, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        return str(join(lst, ', '))

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return str(join(lst, ', '))


class Download(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    downloadable = models.FileField(upload_to="dl/")
    tags = models.ManyToManyField(Tag, blank=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.downloadable.name)
        return extension

