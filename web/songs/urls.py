from django.conf.urls import url
from songs.views import *

urlpatterns = [
    url(r"^$", list_songs, {}, name="list_songs"),
]
