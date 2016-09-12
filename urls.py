from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.defaults import page_not_found, server_error
from media.views import downloads, behind_the_music, upload

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('marketing.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^members/', include('members.urls')),
    url(r'^shows/', include('shows.urls')),
    url(r'^songs/', include('songs.urls')),
    url(r'^photos/', include('media.urls')),
    url(r'^fidouche/', include('fidouche.urls')),
    url(r'^setter/', include('setter.urls')),
    url(r'^downloads/', downloads),
    url(r'^behind-the-music/', behind_the_music),
    url(r'^media/upload/', upload),
    # Legacy redirects
    url(r'^upcoming-shows/', RedirectView.as_view(url='/shows', permanent=True)),
    url(r'^past-shows/', RedirectView.as_view(url='/shows/past', permanent=True)),
    url(r'^song-list/', RedirectView.as_view(url='/songs', permanent=True)),
    url(r'^news-press/', RedirectView.as_view(url='/', permanent=True)),
    url(r'^quotes/', RedirectView.as_view(url='/about#quotes', permanent=True)),
    url(r'^catalog/', RedirectView.as_view(url='http://v2.foreverland.com/catalog/', permanent=True)),
    url(r'^theworks/', RedirectView.as_view(url='http://v2.foreverland.com/theworks/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]
