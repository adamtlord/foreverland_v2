from songs.models import Song
from rest_framework import serializers
from members.serializers import MemberSerializer


class SongSerializer(serializers.HyperlinkedModelSerializer):
    singer = MemberSerializer(many=True)

    class Meta:
        model = Song
        exclude = ('display',)
