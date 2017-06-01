from songs.models import Song, Setlist, Set
from rest_framework import serializers
from members.serializers import SingerSerializer


class SongSerializer(serializers.HyperlinkedModelSerializer):
    singers = SingerSerializer(many=True)

    class Meta:
        model = Song
        exclude = ('display',)


class SetSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Set
        fields = ('songs', 'order')


class SetlistSerializer(serializers.HyperlinkedModelSerializer):
    sets = SetSerializer(many=True)
    name = serializers.CharField(source="__unicode__")

    class Meta:
        model = Setlist
        fields = ('name', 'show', 'sets')
