from django.shortcuts import render
from rest_framework import viewsets

from songs.models import Song
from songs.serializers import SongSerializer


def list_songs(request, template='songs/song_list.html'):
    """just show all the songs"""
    songs = Song.objects.filter(display=True).order_by('name')
    d = {}
    d['songs'] = songs
    return render(request, template, d)


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Members to be viewed or edited.
    """
    queryset = Song.objects.filter(display=True).order_by('name')
    serializer_class = SongSerializer
    filter_fields = ('singer', 'original_album',)
