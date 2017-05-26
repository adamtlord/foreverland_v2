from shows.models import Show, Venue
from rest_framework import serializers


class VenueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Venue
        fields = '__all__'


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = Show
        fields = (
            'public',
            'venue',
            'date',
            'notes',
        )
