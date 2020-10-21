from django.shortcuts import render
from members.models import Member


def list_members(request, template='members/members_list.html'):
    """just show all the members"""
    members = Member.objects.filter(active=True)
    d = {}
    d['members'] = members
    return render(request, template, d)

