from members.models import Member, Sub
from rest_framework import serializers


class SingerSerializer(serializers.HyperlinkedModelSerializer):
    first = serializers.CharField(source='display_first')
    last = serializers.CharField(source='display_last')

    class Meta:
        model = Member
        fields = (
            'url',
            'first',
            'last',
        )


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Member
        exclude = ('bio', 'dob', 'ssn', 'date_partner_joined', 'date_partner_left')


class SubSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sub
        exclude = ('ssn',)
