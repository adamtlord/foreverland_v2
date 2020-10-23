from django.conf.urls import url
from media.views import *

urlpatterns = [
    url(r"^$", photos, {}, name="photos"),
    url(r"^image/(\d+)/$", image, {}, name="image"),
    url(r"^update/$", update, {}, name="update"),
    url(r"^search/$", search, {}, name="search"),
]
