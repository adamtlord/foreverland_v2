from django.urls import path
from media.views import photos

urlpatterns = [
    path("", photos, {}, name="photos"),
]
