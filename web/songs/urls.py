from django.urls import path
from songs.views import list_songs

urlpatterns = [
    path("", list_songs, name="list_songs"),
]
