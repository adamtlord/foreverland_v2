from django.conf.urls import url
from members.views import *

urlpatterns = [
    url(r'^$', list_members, {}, name='list_members'),
]
