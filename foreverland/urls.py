from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.defaults import page_not_found, server_error
from django.contrib import admin

from media.views import downloads, behind_the_music, upload
from rest_framework import routers

# API
from members.views import MemberViewSet, SubViewSet
from songs.views import SongViewSet, SetlistViewSet
from shows.views import ShowViewSet, VenueViewSet

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'subs', SubViewSet)
router.register(r'songs', SongViewSet)
router.register(r'setlists', SetlistViewSet)
router.register(r'shows', ShowViewSet)
router.register(r'venues', VenueViewSet)

# WEB
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
    url(r'^downloads/', downloads),
    url(r'^behind-the-music/', behind_the_music),
    url(r'^media/upload/', upload, name='media_upload'),
    url(r'^_nested_admin/', include('nested_admin.urls')),
    # API
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
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
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]
