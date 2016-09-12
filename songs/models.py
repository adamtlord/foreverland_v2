from django.db import models
from members.models import Member
from shows.models import Show


class Song(models.Model):
    # Song info
    name = models.CharField(max_length=200, blank=True, null=True)
    original_artist = models.CharField(max_length=200, blank=True, null=True)
    original_album = models.CharField(max_length=200, blank=True, null=True)
    release_year = models.CharField(max_length=200, blank=True, null=True)
    display = models.BooleanField(default=True)
    # Foreverland info
    singer = models.ManyToManyField(Member, related_name='singer', blank=True)
    foh_notes = models.TextField(verbose_name="Notes for FOH", blank=True, null=True)

    def __unicode__(self):
        return self.name


class Setlist(models.Model):
    show = models.ForeignKey(Show, related_name='setlist')
    songs = models.ManyToManyField(Song, through='SetlistSong')

    def __unicode__(self):
        return '%s %s' % (self.show.date.strftime('%d/%m/%y'), self.show.venue)


class SetlistSong(models.Model):
    song = models.ForeignKey(Song)
    setlist = models.ForeignKey(Setlist)
    order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.song
