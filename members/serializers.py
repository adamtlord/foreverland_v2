from members.models import Member, Sub
from rest_framework import serializers


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Member
        exclude = ('bio', 'dob', 'ssn', 'date_partner_joined', 'date_partner_left')


class SubSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sub
        exclude = ('ssn',)
