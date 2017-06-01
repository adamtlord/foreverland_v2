from django.shortcuts import render
from rest_framework import viewsets
from members.models import Member, Sub
from members.serializers import MemberSerializer, SubSerializer


def list_members(request, template='members/members_list.html'):
    """just show all the members"""
    members = Member.objects.filter(active=True)
    d = {}
    d['members'] = members
    return render(request, template, d)


class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Members to be viewed or edited.
    """
    queryset = Member.objects.all().order_by('-join_date')
    serializer_class = MemberSerializer
    filter_fields = ('active', 'partner', 'section',)


class SubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Subs to be viewed or edited.
    """
    queryset = Sub.objects.all().order_by('-last_name')
    serializer_class = SubSerializer
    filter_fields = ('instrument',)
