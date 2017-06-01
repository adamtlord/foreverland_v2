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
    singers = models.ManyToManyField(Member, related_name='singer', blank=True)
    foh_notes = models.TextField(verbose_name="Notes for FOH", blank=True, null=True)
    bpm = models.PositiveSmallIntegerField(blank=True, null=True)
    solos = models.ManyToManyField(Member, related_name='soloist', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-display', 'name']


class Setlist(models.Model):
    show = models.ForeignKey(Show, related_name='setlist')

    def __unicode__(self):
        return '%s %s' % (self.show.date.strftime('%d/%m/%y'), self.show.venue)


class Set(models.Model):
    setlist = models.ForeignKey(Setlist, related_name='sets')
    songs = models.ManyToManyField(Song, through='SetSong')
    order = models.PositiveSmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s Set %s' % (self.setlist, self.order)

    class Meta:
        ordering = ['order']


class SetSong(models.Model):
    song = models.ForeignKey(Song, blank=True, null=True)
    set = models.ForeignKey(Set, blank=True, null=True)
    order = models.PositiveSmallIntegerField(blank=True, null=True)
    transition = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % self.song

    class Meta:
        ordering = ['order']
